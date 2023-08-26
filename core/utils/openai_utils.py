import openai
import tiktoken
import json

from core.config import config
from core.utils.function_utils import functions, function, property, PropertyType
from core.utils.function_utils import fns_collection

# setup openai
openai.api_key = config.openai_api_key
if config.openai_api_base is not None:
    openai.api_base = config.openai_api_base

OPENAI_COMPLETION_OPTIONS = {
    "temperature": 1,
    "max_tokens": 1000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "functions": [],  # list of functions without params
}

OPENAI_COMPLETION_OPTIONS['functions'] = fns_collection.to_json_without_params()
# OPENAI_COMPLETION_OPTIONS['functions'] = [f.to_json()]

# used to call a specific function.
# we will set 1 specific function with params here, via:
# generate_fn_call_options(your_function: function) -> dict:
OPENAI_FUNCTION_CALL_OPTIONS = {
    "temperature": 0,
    "max_tokens": 1000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "functions": [],
    "function_call": {}
}


class ChatGPT:
    def __init__(self, model=config.openai_model):
        assert model in {"text-davinci-003", "gpt-3.5-turbo-16k", "gpt-3.5-turbo", "gpt-4"}, f"Unknown model: {model}"
        self.model = model

    async def send_message(self, message, dialog_messages=[], chat_mode="assistant"):
        n_dialog_messages_before = len(dialog_messages)
        answer = None
        fn_call_res = None
        while answer is None:
            try:
                if self.model in {"gpt-3.5-turbo-16k", "gpt-3.5-turbo", "gpt-4"}:
                    messages = self._generate_prompt_messages(message, dialog_messages, chat_mode)
                    r = await openai.ChatCompletion.acreate(
                        model=self.model,
                        messages=messages,
                        **OPENAI_COMPLETION_OPTIONS
                    )
                    answer = r.choices[0].message["content"]
                    if "function_call" in r.choices[0].message:
                        fn_name = r.choices[0].message["function_call"]["name"]
                        fns_collection[fn_name].trigger_fn()
                        # here we got function suggestion without params.
                        # use trigger_fn to trigger ui flow here to get params from user.
                        # below, we will call specific function with params.
                        # swap messages[-1]["content"] to user input. this is "last user message".
                        if fn_name in fns_collection:
                            fn_call_res = await self.send_function_call(
                                your_function=fns_collection[fn_name], 
                                input=messages[-1]["content"],
                                chat_mode=chat_mode
                            )
                            answer = str(fn_call_res)

                answer = self._postprocess_answer(answer)
                n_input_tokens, n_output_tokens = r.usage.prompt_tokens, r.usage.completion_tokens
            except openai.error.InvalidRequestError as e:  # too many tokens
                if len(dialog_messages) == 0:
                    raise ValueError(
                        "Dialog messages is reduced to zero, but still has too many tokens to make completion") from e

                # forget first message in dialog_messages
                # dialog_messages = dialog_messages[1:]
                # context management later.

        n_first_dialog_messages_removed = n_dialog_messages_before - len(dialog_messages)

        return answer, (n_input_tokens, n_output_tokens), n_first_dialog_messages_removed

    # used to call specific function. args:
    # function_utils.function - with params
    # input - user message containing info for function call
    async def send_function_call(self, your_function: function, input: str, chat_mode="assistant"):
        r = None
        fn_call_res = None
        while r is None:
            if self.model in {"gpt-3.5-turbo-16k", "gpt-3.5-turbo", "gpt-4"}:
                messages = self.generate_fn_call_messages(input, chat_mode)
                r = await openai.ChatCompletion.acreate(
                    model=self.model,
                    messages=messages,
                    **self.generate_fn_call_options(your_function)
                )
                # answer = r.choices[0].message["content"]
                if "function_call" in r.choices[0].message:
                    fn_name = r.choices[0].message["function_call"]["name"]
                    try:
                        fn_args = json.loads(r.choices[0].message["function_call"]["arguments"])
                        if fn_name in fns_collection:
                            fn_call_res = fns_collection[fn_name].fn(**fn_args)  # function call
                            # fn_call_res = str(r.choices[0].message["function_call"])  # use this for testing
                    except json.decoder.JSONDecodeError as e:
                        print("Error decoding json:", r.choices[0].message["function_call"]["arguments"])
                        raise e
                else:
                    raise ValueError("No function call in response")

        return fn_call_res

    def _generate_prompt(self, message, dialog_messages, chat_mode):
        prompt = config.chat_modes[chat_mode]["prompt_start"]
        prompt += "\n\n"

        # add chat context
        if len(dialog_messages) > 0:
            prompt += "Chat:\n"
            for dialog_message in dialog_messages:
                prompt += f"User: {dialog_message['user']}\n"
                prompt += f"Assistant: {dialog_message['bot']}\n"

        # current message
        prompt += f"User: {message}\n"
        prompt += "Assistant: "

        return prompt

    def _generate_prompt_messages(self, message, dialog_messages, chat_mode):
        prompt = config.chat_modes[chat_mode]["prompt_start"]

        messages = [{"role": "system", "content": prompt}]
        for dialog_message in dialog_messages:
            messages.append({"role": "user", "content": dialog_message["user"]})
            messages.append({"role": "assistant", "content": dialog_message["bot"]})
        messages.append({"role": "user", "content": message})

        return messages
    
    def generate_fn_call_messages(self, input: str, chat_mode) -> list:
        prompt = config.chat_modes[chat_mode]["prompt_start"]

        messages = [{"role": "system", "content": prompt}]  # work on prompt mb
        messages.append({"role": "user", "content": input})

        return messages

    def generate_fn_call_options(self, your_function: function) -> dict:
        OPENAI_FUNCTION_CALL_OPTIONS['functions']=[your_function.to_json()]
        OPENAI_FUNCTION_CALL_OPTIONS['function_call']={'name': your_function.name}
        return OPENAI_FUNCTION_CALL_OPTIONS

    def _postprocess_answer(self, answer):
        answer = answer.strip()
        return answer

    def _count_tokens_from_messages(self, messages, answer, model=config.openai_model):
        encoding = tiktoken.encoding_for_model(model)

        if model == "gpt-3.5-turbo-16k":
            tokens_per_message = 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif model == "gpt-3.5-turbo":
            tokens_per_message = 4
            tokens_per_name = -1
        elif model == "gpt-4":
            tokens_per_message = 3
            tokens_per_name = 1
        else:
            raise ValueError(f"Unknown model: {model}")

        # input
        n_input_tokens = 0
        for message in messages:
            n_input_tokens += tokens_per_message
            for key, value in message.items():
                n_input_tokens += len(encoding.encode(value))
                if key == "name":
                    n_input_tokens += tokens_per_name

        n_input_tokens += 2

        # output
        n_output_tokens = 1 + len(encoding.encode(answer))

        return n_input_tokens, n_output_tokens

    def _count_tokens_from_prompt(self, prompt, answer, model="text-davinci-003"):
        encoding = tiktoken.encoding_for_model(model)

        n_input_tokens = len(encoding.encode(prompt)) + 1
        n_output_tokens = len(encoding.encode(answer))

        return n_input_tokens, n_output_tokens
