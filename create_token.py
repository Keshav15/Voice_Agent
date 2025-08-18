import os
from fastapi import FastAPI, Query
from livekit import api
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # Load LIVEKIT_API_KEY and LIVEKIT_API_SECRET from .env

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to frontend origin
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
        api.VideoGrants(
            room_join=True,
            room=room
        )
    )
    return {"token": token.to_jwt()}

@app.get("/v1/health")
def health_check():
    return {"status": "ok"}

# Run directly with: python token.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

