import os
from fastapi import FastAPI, Query
from livekit import api
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

load_dotenv()

# FIX 1: This handles the API Gateway stage name (e.g., /default)
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/getToken")
def get_token(room: str = Query(...), identity: str = Query(...)):
    token = api.AccessToken(
        os.getenv("LIVEKIT_API_KEY"),
        os.getenv("LIVEKIT_API_SECRET")
    ).with_identity(identity).with_name(identity).with_grants(
        # FIX 2: This uses the correct 'VideoGrant' class
        api.VideoGrants(
            room_join=True,
            room=room
        )
    )
    return {"token": token.to_jwt()}

@app.get("/v1/health")
def health_check():
    return {"status": "ok"}

# This is the AWS Lambda entry point
handler = Mangum(app)
