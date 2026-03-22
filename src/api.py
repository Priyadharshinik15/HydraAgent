from fastapi import FastAPI
from pydantic import BaseModel
from agent import WaterIntakeAgent
from database import log_intake, get_intake_history
from logger import log_message
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI()

# ✅ Add these two lines
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def serve_dashboard():
    return FileResponse("water_tracker_dashboard.html")

agent = WaterIntakeAgent()


class WaterIntakeRequest(BaseModel):
    user_id: str
    intake_ml: int


@app.post("/log-intake")
async def log_water_intake(request: WaterIntakeRequest):
    log_intake(request.user_id, request.intake_ml)

    analysis = agent.analyze_intake(request.intake_ml)

    log_message(f"user {request.user_id} logged {request.intake_ml} ml")

    return {
        "message": "Water intake logged successfully",
        "analysis": analysis
    }


@app.get("/history/{user_id}")
async def get_water_history(user_id: str):
    history = get_intake_history(user_id)
    return {"history": history}