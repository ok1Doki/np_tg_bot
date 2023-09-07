import base64
import uuid

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from core.assistant.assistant_service import handle_json_from_user, handle_audio_from_user
from core.audio_handling.audio_generation_service import convert_text_to_audio
from core.utils.enums import Role, MessageType
from core.utils.file_utils import persist_binary_file_locally

controller = APIRouter(prefix='/voice-assistant')

connections_pool = {}


@controller.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    conn_id = await create_websocket_connection(websocket)
    pass


async def create_websocket_connection(websocket):
    connection_id = str(uuid.uuid4())
    connections_pool[connection_id] = websocket
    await start_listening(connection_id)
    return connection_id


async def start_listening(session_id):
    socket = connections_pool[session_id]
    await socket.accept()
    try:
        while True:
            data = await socket.receive()
            if 'text' in data:
                await handle_json_from_user(session_id, data['text'])
            if 'bytes' in data:
                await handle_audio_from_user(session_id, data['bytes'])
    except WebSocketDisconnect:
        del connections_pool[session_id]
    finally:
        del connections_pool[session_id]


async def send_message(conn_id: str, message: str, role: Role, with_audio: bool = False):
    message_obj = {"role": role, "type": MessageType.TEXT, "data": message}
    await connections_pool[conn_id].send_json(message_obj)

    # if with_audio:
    #     generated_audio_ai = convert_text_to_audio(message)
    #     output_audio_local_file_path = persist_binary_file_locally(
    #         data=generated_audio_ai.audio_content,
    #         file_suffix='ai_audio_reply.mp3'
    #     )
    #     await send_audio(conn_id, output_audio_local_file_path)


async def send_audio(conn_id: str, audio_file_path: str):
    with open(audio_file_path, "rb") as audio_file:
        audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode("utf-8")
        await connections_pool[conn_id].send_json({"role": Role.BOT, "type": MessageType.AUDIO, "data": audio_base64})
