import core.utils.openai_utils as openai_utils

# used only for audio?
async def generate_llm_response(user_prompt: str,
                                dialog_messages: tuple) -> tuple:
    chatgpt_instance = openai_utils.ChatGPT(model='gpt-3.5-turbo-16k')
    answer = await chatgpt_instance.send_message(user_prompt, dialog_messages=dialog_messages)
    return answer
