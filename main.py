import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ 允許你的前端來源（部署後請換成你的實際網址）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cici20050710-collab.github.io"
    ],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)
# ✅ API Key 從環境變數讀取，不寫死在程式碼裡
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


class AnalyzeRequest(BaseModel):
    base64Image: str      # 前端傳來的 base64 圖片
    lipList: list
    eyeList: list
    baseList: list


@app.post("/api/analyze")
async def analyze(req: AnalyzeRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="伺服器未設定 API Key")

    system_prompt = (
        "You are a professional makeup AI. Analyze the user skin tone and face. "
        "Pick ONE from each list. "
        f"Lip list: {req.lipList}. "
        f"Eye list: {req.eyeList}. "
        f"Base list: {req.baseList}. "
        "Return ONLY JSON with keys: skin_tone, face_shape, "
        "recommended_lip_id, recommended_eye_id, recommended_base_id, advice. "
        "No markdown, no extra text."
    )

    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{
            "parts": [
                {"text": "Analyze my face and recommend colors. Return only JSON."},
                {"inline_data": {"mime_type": "image/jpeg", "data": req.base64Image}}
            ]
        }],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 300}
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Gemini API 錯誤：{response.text}"
        )

    return response.json()
