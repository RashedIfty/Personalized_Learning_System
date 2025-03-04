import openai
from app.core.config import settings
from app.prompts.prompts import (
    EXTRACT_QUESTIONS_SYSTEM_PROMPT,
    EXTRACT_QUESTIONS_USER_PROMPT,
    GENERATE_ANSWERS_SYSTEM_PROMPT,
    GENERATE_ANSWERS_USER_PROMPT,
)

def extract_questions_from_book(book_text: str):
    """Extract questions from a book using GPT-4o."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": EXTRACT_QUESTIONS_SYSTEM_PROMPT},
                {"role": "user", "content": EXTRACT_QUESTIONS_USER_PROMPT.format(book_text=book_text[:4000])},
            ]
        )
        questions = response.choices[0].message.content.split("\n")
        extracted_questions = [q.strip() for q in questions if len(q.strip()) > 5]
        return extracted_questions
    except Exception as e:
        raise RuntimeError(f"Error extracting questions: {str(e)}")

def generate_answers_from_book(book_text: str, questions: list):
    """Generate answers for extracted questions using GPT-4o."""
    answers = []
    for question in questions:
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": GENERATE_ANSWERS_SYSTEM_PROMPT},
                    {"role": "user", "content": GENERATE_ANSWERS_USER_PROMPT.format(
                        book_text=book_text[:4000],
                        question=question
                    )},
                ]
            )
            answers.append({"question": question, "answer": response.choices[0].message.content.strip()})
        except Exception as e:
            raise RuntimeError(f"Error generating answer: {str(e)}")
    
    return answers
