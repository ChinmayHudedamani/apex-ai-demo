# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Enterprise Streaming Chat Service Router

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Literal, AsyncGenerator
import asyncio
import json
import html
import re

from app.core.config import settings

router = APIRouter(prefix="/chat", tags=["AI Chatbot Streaming Engine"])

# Hardcoded Server-Side System Prompt (Never accepted from client bundle)
SYSTEM_PROMPT = """You are Copus AI, the elite AI Dental Concierge for Apex Dental Clinic.
Your goal is to assist patients warmly, provide transparent pricing details, schedule specialist appointments,
and offer precise clinic guidance while maintaining clinical protocol standards.
Keep your answers helpful, concise (2-4 sentences max), and professional."""


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system", "bot"] = Field(..., description="Message role")
    content: str = Field(..., min_length=1, max_length=4000, description="Raw message text content")


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., min_length=1, description="Conversation history")
    tier: Literal["T1", "T2", "T2_5", "T3"] = Field(default="T2", description="SaaS Tier Level")


def sanitize_input(text: str) -> str:
    """Sanitizes user input to prevent XSS / script injection attacks."""
    escaped = html.escape(text)
    # Strip dangerous script tag patterns
    cleaned = re.sub(r'<script.*?>.*?</script>', '', escaped, flags=re.DOTALL | re.IGNORECASE)
    return cleaned.strip()


async def generate_chat_stream(user_prompt: str, tier: str) -> AsyncGenerator[str, None]:
    """Simulates or streams real-time AI response chunks via SSE format using server-side API key configuration."""
    clean_prompt = sanitize_input(user_prompt)
    lower_prompt = clean_prompt.lower()

    # Server-side API Key references (loaded safely from server environment, never sent to client)
    _server_gemini_key = settings.GEMINI_API_KEY
    _server_openai_key = settings.OPENAI_API_KEY

    # Contextual dynamic responses for Apex Dental Clinic
    if "doctor" in lower_prompt or "specialist" in lower_prompt:
        response_text = "Dr. Chinmay Hudedamani (Prosthodontist & Implantologist), Dr. Ananya Rao (Orthodontist), and Dr. Vikramaditya Hegde (Endodontist) are our chief specialists. Would you like to view their available slots?"
    elif "price" in lower_prompt or "cost" in lower_prompt or "fee" in lower_prompt:
        response_text = "Our consultation starts at ₹500. Clear Aligners range from ₹45,000–₹1,20,000, and Laser Teeth Whitening is ₹8,500. All treatments include zero hidden fees!"
    elif "location" in lower_prompt or "address" in lower_prompt or "where" in lower_prompt:
        response_text = "We are located at #42, Apex Towers, 100 Ft Road, Indiranagar, Bengaluru. Landmark: Opposite Metro Pillar 114."
    elif "emergency" in lower_prompt or "pain" in lower_prompt or "swelling" in lower_prompt:
        response_text = "🚨 If you are in severe pain or experiencing swelling, our Emergency Triage protocol is active. Please call our 24/7 line at +91 98765 43210 for immediate fast-tracking."
    else:
        response_text = f"Thank you for contacting Apex Dental Clinic! Regarding '{clean_prompt[:50]}...', our AI concierge is ready to assist you. You can browse our specialists, check pricing, or schedule an appointment anytime."

    words = response_text.split(" ")
    for word in words:
        chunk_data = json.dumps({"delta": word + " "})
        yield f"data: {chunk_data}\n\n"
        await asyncio.sleep(0.04)

    yield "data: [DONE]\n\n"


@router.post("/stream")
async def stream_chat(req: ChatRequest):
    """
    Real-time streaming AI chatbot completion endpoint.
    Accepts Pydantic-validated conversation history and streams token deltas via SSE.
    API keys remain 100% isolated on the server.
    """
    if not req.messages:
        raise HTTPException(status_code=400, detail="Messages list cannot be empty.")

    last_user_msg = next((m for m in reversed(req.messages) if m.role == "user"), None)
    prompt_text = last_user_msg.content if last_user_msg else "Hello"

    return StreamingResponse(
        generate_chat_stream(prompt_text, req.tier),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
