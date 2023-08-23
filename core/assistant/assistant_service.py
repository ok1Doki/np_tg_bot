from datetime import datetime

from core.audio_handling.audio_generation_service import convert_text_to_audio
from core.audio_handling.audio_transcription_service import convert_audio_to_text
from core.chat.chat_service import generate_llm_response
from core.utils.file_utils import persist_binary_file_locally, get_transcoded_audio_file_path

messages_history = {}


async def handle_audio_from_user(session_id: str,
                                 file: bytes,
                                 user_text_callback=None,
                                 ai_text_callback=None,
                                 ai_audio_callback=None) -> str:
    if session_id not in messages_history:
        messages_history[session_id] = []

    transcoded_user_audio_file_path = get_transcoded_audio_file_path(file)
    user_message = await convert_audio_to_text(transcoded_user_audio_file_path)
    if user_text_callback is not None:
        await user_text_callback(user_message)

    ai_text_reply, (n_input_tokens, n_output_tokens), n_first_dialog_messages_removed = await generate_llm_response(
        user_message, messages_history[session_id])
    if ai_text_callback is not None:
        await ai_text_callback(ai_text_reply)

    messages_history[session_id].append({"user": user_message, "bot": ai_text_reply, "data": datetime.now()})

    generated_audio_ai = convert_text_to_audio(ai_text_reply)
    output_audio_local_file_path = persist_binary_file_locally(
        data=generated_audio_ai.audio_content,
        file_suffix='ai_audio_reply.mp3'
    )
    if ai_audio_callback is not None:
        await ai_audio_callback(output_audio_local_file_path)

    return output_audio_local_file_path


async def handle_json_from_user(session_id: str,
                                json_data: str,
                                user_text_callback=None,
                                ai_text_callback=None,
                                ai_audio_callback=None) -> str:
    pass
