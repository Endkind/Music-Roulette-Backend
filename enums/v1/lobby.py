from enum import Enum


class LobbyRequestType(Enum):
    JOIN = "join"
    LEAVE = "leave"
    MESSAGE = "message"
    SUBMIT_SONGS = "submit_songs"
