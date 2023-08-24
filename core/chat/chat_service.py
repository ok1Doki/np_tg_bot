import core.utils.openai_utils as openai_utils
from core.config.config import OPENAI_FUNCTION_CALL_OPTIONS
from core.utils.function_utils import functions, function, property, PropertyType


async def generate_llm_response(user_prompt: str,
                                dialog_messages: tuple) -> tuple:
    chatgpt_instance = openai_utils.ChatGPT(model='gpt-3.5-turbo-16k')
    answer = await chatgpt_instance.send_message(user_prompt, dialog_messages=dialog_messages)
    return answer


def get_function_call_options(your_function: function) -> dict:
    OPENAI_FUNCTION_CALL_OPTIONS['functions']=[your_function.to_json()]
    OPENAI_FUNCTION_CALL_OPTIONS['function_call']['name']=your_function.name
    return OPENAI_FUNCTION_CALL_OPTIONS
