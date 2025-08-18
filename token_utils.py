# token_utils.py
import os
from livekit import api
from dotenv import load_dotenv

load_dotenv()

def generate_token(room: str, identity: str) -> str:
    token = api.AccessToken(
        os.getenv("LIVEKIT_API_KEY"),
        os.getenv("LIVEKIT_API_SECRET")
    ).with_identity(identity).with_name(identity).with_grants(
        api.VideoGrants(
            room_join=True,
            room=room
        )
    )
    return token.to_jwt()
