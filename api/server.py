from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
import threading
import uvicorn

app = FastAPI()
engine = None # Will be set by main.py

class CallRequest(BaseModel):
    destination: str

class RegisterRequest(BaseModel):
    server: str
    username: str
    password: str

@app.post("/api/register")
async def register(req: RegisterRequest):
    try:
        engine.register(req.server, req.username, req.password)
        return {"status": "Registration initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/call")
async def make_call(req: CallRequest):
    try:
        engine.make_call(req.destination)
        return {"status": "Calling " + req.destination}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/hangup")
async def hangup():
    try:
        engine.hangup()
        return {"status": "Hanging up"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def get_status():
    if not engine.acc:
        return {"status": "Unregistered"}
    info = engine.acc.getInfo()
    return {
        "status": "Registered" if info.regIsActive else "Unregistered",
        "active_call": engine.current_call is not None
    }

def start_api(sip_engine, host="127.0.0.1", port=8000):
    global engine
    engine = sip_engine
    uvicorn.run(app, host=host, port=port)
