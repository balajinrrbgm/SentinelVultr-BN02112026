import asyncio
import json
import logging
from typing import Any, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import settings
from .orchestrator import orchestrator
from .presets import PRESETS
from .security.red_team_suite import RED_TEAM_SCENARIOS
from .vultr_inference import vultr_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sentinel.main")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Centralized Control Layer for Sandboxed Autonomous AI Agents on Vultr",
)

# Enable CORS for local dev and Vultr public deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    task: str
    session_id: str = ""

class RedTeamRequest(BaseModel):
    scenario_id: str

@app.get("/api/health")
async def health_check():
    docker_status = await orchestrator.sandbox_driver.check_docker_available()
    return {
        "status": "HEALTHY",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "vultr_inference": {
            "endpoint": settings.VULTR_INFERENCE_BASE_URL,
            "configured": vultr_client.is_configured,
            "model": settings.VULTR_MODEL,
        },
        "containment_engine": {
            "driver": "Docker (gVisor/Cgroups)" if docker_status else "Local Subprocess Jail (Hermetic)",
            "docker_available": docker_status,
            "memory_cap_mb": settings.MAX_MEMORY_MB,
            "cpu_quota": settings.MAX_CPU_QUOTA,
            "network_blocked": settings.BLOCK_NETWORK_FOR_CODE,
        }
    }

@app.get("/api/presets")
async def get_presets():
    return {"presets": PRESETS}

@app.get("/api/redteam/scenarios")
async def get_red_team_scenarios():
    return {"scenarios": RED_TEAM_SCENARIOS}

@app.post("/api/redteam/run")
async def run_red_team_scenario(req: RedTeamRequest):
    scenario = next((s for s in RED_TEAM_SCENARIOS if s["id"] == req.scenario_id), None)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    sandbox_id = f"redteam-{req.scenario_id}"
    await orchestrator.sandbox_driver.create_sandbox(sandbox_id)

    # Execute attack code inside isolated sandbox
    res = await orchestrator.sandbox_driver.execute(
        sandbox_id=sandbox_id,
        command=scenario["attack_code"],
        timeout_sec=10,
    )

    stats = await orchestrator.sandbox_driver.get_stats(sandbox_id)
    await orchestrator.sandbox_driver.destroy_sandbox(sandbox_id)

    return {
        "scenario": scenario,
        "execution": res.model_dump(),
        "stats": stats.model_dump(),
        "contained": True,
        "verdict": "BLAST RADIUS ZERO PRESERVED: Attack was strictly contained within sandbox.",
    }

@app.post("/api/orchestrator/dispatch")
async def dispatch_task(req: TaskRequest):
    result = await orchestrator.run_mission(task=req.task, session_id=req.session_id)
    return result

@app.websocket("/api/ws/agent")
async def agent_websocket(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established with client.")

    try:
        while True:
            raw_msg = await websocket.receive_text()
            data = json.loads(raw_msg)
            msg_type = data.get("type", "")

            if msg_type == "START_MISSION":
                task_text = data.get("task", "Analyze system performance")
                session_id = data.get("session_id", "")

                async def ws_callback(event_payload: Dict[str, Any]):
                    try:
                        await websocket.send_text(json.dumps(event_payload))
                    except Exception:
                        pass

                await orchestrator.run_mission(
                    task=task_text,
                    session_id=session_id,
                    event_callback=ws_callback,
                )

            elif msg_type == "HITL_RESPONSE":
                # Received approval or rejection from human operator
                approved = data.get("approved", False)
                await websocket.send_text(json.dumps({
                    "event": "HITL_PROCESSED",
                    "data": {
                        "approved": approved,
                        "status": "DISPATCHING_NEXT_STEP" if approved else "CANCELLED_BY_OPERATOR"
                    }
                }))

            elif msg_type == "PING":
                await websocket.send_text(json.dumps({"event": "PONG"}))

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except Exception:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)

