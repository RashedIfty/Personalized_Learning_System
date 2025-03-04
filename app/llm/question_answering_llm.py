import openai
from app.core.config import settings
from app.prompts.prompts import QUESTION_ANSWERING_SYSTEM_PROMPT, QUESTION_ANSWERING_USER_PROMPT

def generate_answer(book_text: str, question: str) -> str:
    """Generate an answer using GPT-4o based on the book text."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": QUESTION_ANSWERING_SYSTEM_PROMPT},
                {"role": "user", "content": QUESTION_ANSWERING_USER_PROMPT.format(book_text=book_text[:4000], question=question)}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Error generating answer: {str(e)}")
