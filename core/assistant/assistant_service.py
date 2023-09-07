from datetime import datetime

import core.config as config
import core.utils.openai_utils as openai_utils
import core.assistant.assistant_controller as sock
from core.audio_handling.audio_transcription_service import convert_audio_to_text
from core.utils.enums import Role
from core.utils.file_utils import get_transcoded_audio_file_path
from core.utils.function_utils import function

messages_history = {}


async def handle_audio_from_user(session_id: str,
                                 file: bytes) -> None:
    if session_id not in messages_history:
        messages_history[session_id] = []

    transcoded_user_audio_file_path = get_transcoded_audio_file_path(file)
    user_message = await convert_audio_to_text(transcoded_user_audio_file_path)
    await sock.send_message(session_id, user_message, role=Role.USER, with_audio=False)

    chatgpt_instance = openai_utils.ChatGPT(model=config.openai_model)
    ai_text_reply, (n_input_tokens, n_output_tokens), n_first_dialog_messages_removed = \
        await chatgpt_instance.send_message(user_message,
                                            # session_id,
                                            dialog_messages=messages_history[session_id],
                                            trigger_fn=function_trigger)

    await sock.send_message(conn_id=session_id, message=ai_text_reply, role=Role.BOT, with_audio=True)

    messages_history[session_id].append(
        {"session": session_id, "user": user_message, "bot": ai_text_reply, "time": datetime.now()})


async def function_trigger(connection_id: str, fun: function) -> str:
    response = await sock.send_message(conn_id=connection_id, message=str(fun.properties), role=Role.BOT, with_audio=True)
    return response


async def handle_json_from_user(session_id: str,
                                json_data: str) -> str:
    pass
