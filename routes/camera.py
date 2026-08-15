from fastapi import APIRouter, HTTPException
from services.camera_service import CameraService

router = APIRouter(prefix="/api/camera", tags=["camera"])
camera = CameraService()

@router.post("/start")
async def start_camera(camera_index: int = 0):
    success = camera.start(camera_index)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to start camera")
    return {"status": "started"}

@router.post("/stop")
async def stop_camera():
    camera.stop()
    return {"status": "stopped"}

@router.get("/frame")
async def get_frame():
    frame = camera.get_frame()
    if frame is None:
        raise HTTPException(status_code=404, detail="No frame available")
    processed = camera.process_frame(frame)
    return processed

@router.get("/status")
async def camera_status():
    return {
        "is_running": camera.is_running,
        "fps": camera.fps,
    }
