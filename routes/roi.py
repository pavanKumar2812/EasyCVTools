from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import io, json

from utils.image_utils import get_roi_from_image

router = APIRouter()

@router.post("/generate_roi/")  # ✅ Proper decorator syntax with parentheses
async def generate_roi(file: UploadFile = File(...), points: str = File(...)):
    try:
        points = json.loads(points)
        contents = await file.read()
        roi_image = get_roi_from_image(contents, points)
        return StreamingResponse(io.BytesIO(roi_image), media_type="image/jpeg")
    except Exception as e:
        return {"error": str(e)}
