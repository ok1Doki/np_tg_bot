from enum import Enum


class Role(str, Enum):
    USER = 'user'
    BOT = 'bot'
    SYSTEM = 'system'


class MessageType(str, Enum):
    TEXT = 'text'
    AUDIO = 'audio'
    UI_EVENT = 'ui_event'
