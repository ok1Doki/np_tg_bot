import openai


async def convert_audio_to_text(local_input_file_path: str):
    transcription = openai.Audio.transcribe("whisper-1", open(local_input_file_path, 'rb'), language="uk")
    if transcription is None:
        transcription = ""
    return transcription
