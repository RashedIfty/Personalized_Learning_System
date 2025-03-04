import openai
from app.core.config import settings
from app.prompts.prompts import RESEARCH_KEYWORDS_SYSTEM_PROMPT, RESEARCH_KEYWORDS_USER_PROMPT

def extract_keywords_from_text(book_text: str):
    """Extract keywords from a book using GPT-4o."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": RESEARCH_KEYWORDS_SYSTEM_PROMPT},
                {"role": "user", "content": RESEARCH_KEYWORDS_USER_PROMPT.format(book_text=book_text[:4000])}
            ]
        )
        keywords = response.choices[0].message.content.split(", ")
        return [keyword.strip() for keyword in keywords if keyword.strip()]
    except Exception as e:
        raise RuntimeError(f"Error extracting keywords: {str(e)}")
