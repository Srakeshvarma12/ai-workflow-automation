import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

# Using Gemini 1.5 Flash — free tier, fast
model = genai.GenerativeModel("gemini-1.5-flash")

async def process_with_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and get a response."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Gemini API error: {str(e)}")

async def classify_input(input_text: str) -> dict:
    """Classify input and suggest an action."""
    prompt = f"""
    Analyze the following input and respond in this exact format:
    CATEGORY: [category name]
    PRIORITY: [low/medium/high]
    ACTION: [suggested action]
    SUMMARY: [one sentence summary]

    Input: {input_text}
    """
    result = await process_with_gemini(prompt)
    return {"raw": result, "input": input_text}
