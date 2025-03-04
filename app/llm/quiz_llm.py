import openai
from app.core.config import settings
from app.prompts.prompts import QUIZ_GENERATION_SYSTEM_PROMPT, QUIZ_GENERATION_USER_PROMPT

def generate_quiz_questions(book_text: str, num_questions: int):
    """Generate quiz questions and multiple-choice answers using GPT-4o."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": QUIZ_GENERATION_SYSTEM_PROMPT},
                {"role": "user", "content": QUIZ_GENERATION_USER_PROMPT.format(
                    book_text=book_text[:3000],
                    num_questions=num_questions
                )}
            ]
        )
        return response.choices[0].message.content.split("\n")
    except Exception as e:
        raise RuntimeError(f"Error generating quiz questions: {str(e)}")
