from fastapi import FastAPI
from pydantic import BaseModel
from agent import WaterIntakeAgent
from database import log_intake, get_intake_history
from logger import log_message
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="HydraAgent API",
    description="Agentic AI backend for Smart Hydration Monitoring",
    version="1.0.0"
)

# ✅ CORS — allows Streamlit (port 8501) to talk to FastAPI (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = WaterIntakeAgent()


class WaterIntakeRequest(BaseModel):
    user_id: str
    intake_ml: int


@app.get("/")
async def root():
    return {
        "app": "HydraAgent",
        "status": "running",
        "message": "Open Streamlit dashboard at http://localhost:8501"
    }


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
# from fastapi import FastAPI
# from pydantic import BaseModel
# from agent import WaterIntakeAgent
# from database import log_intake, get_intake_history
# from logger import log_message
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse


# app = FastAPI()

# # ✅ Add these two lines
# app.mount("/static", StaticFiles(directory="."), name="static")

# @app.get("/")
# async def serve_dashboard():
#     return FileResponse("water_tracker_dashboard.html")

# agent = WaterIntakeAgent()


# class WaterIntakeRequest(BaseModel):
#     user_id: str
#     intake_ml: int


# @app.post("/log-intake")
# async def log_water_intake(request: WaterIntakeRequest):
#     log_intake(request.user_id, request.intake_ml)

#     analysis = agent.analyze_intake(request.intake_ml)

#     log_message(f"user {request.user_id} logged {request.intake_ml} ml")

#     return {
#         "message": "Water intake logged successfully",
#         "analysis": analysis
#     }


# @app.get("/history/{user_id}")
# async def get_water_history(user_id: str):
#     history = get_intake_history(user_id)
#     return {"history": history}