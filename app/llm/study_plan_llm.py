import openai
from app.core.config import settings
from app.prompts.prompts import STUDY_PLAN_SYSTEM_PROMPT, STUDY_PLAN_USER_PROMPT

def generate_study_plan_from_text(book_text: str, duration: int):
    """Generate a study plan using GPT-4o."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": STUDY_PLAN_SYSTEM_PROMPT},
                {"role": "user", "content": STUDY_PLAN_USER_PROMPT.format(book_text=book_text[:3000], duration=duration)}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Error generating study plan: {str(e)}")
