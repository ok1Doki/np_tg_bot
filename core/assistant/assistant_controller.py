import base64
import uuid

from fastapi import APIRouter, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from core.assistant.assistant_service import handle_json_from_user, handle_audio_from_user
from core.utils.chroma_utils import demo

controller = APIRouter(prefix='/voice-assistant')

connected_clients = {}


@controller.post('/test', status_code=200)
async def test():
    return demo()


@controller.post('/audio-message', status_code=200)
async def handle_receive_audio_data(file: UploadFile):
    file_data = await file.read()
    generated_ai_audio_file_path = await handle_audio_from_user(file_data)
    return FileResponse(generated_ai_audio_file_path, media_type='audio/mpeg', filename='ai_output')


@controller.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    connected_clients[session_id] = websocket

    async def user_text_callback(message):
        message_obj = {"role": "user", "type": "text", "data": message}
        await websocket.send_json(message_obj)

    async def ai_text_callback(message):
        message_obj = {"role": "assistant", "type": "text", "data": message}
        await websocket.send_json(message_obj)

    async def ai_audio_callback(audio_file_path):
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode("utf-8")
            await websocket.send_json({"user": "assistant", "type": "audio", "data": audio_base64})

    try:
        while True:
            data = await websocket.receive()

            if 'text' in data:
                await handle_json_from_user(session_id,
                                            data['text'],
                                            user_text_callback,
                                            ai_text_callback,
                                            ai_audio_callback)
            if 'bytes' in data:
                await handle_audio_from_user(session_id,
                                             data['bytes'],
                                             user_text_callback,
                                             ai_text_callback,
                                             ai_audio_callback)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
