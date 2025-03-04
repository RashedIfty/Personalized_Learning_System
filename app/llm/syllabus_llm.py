import openai
from app.core.config import settings
from app.prompts.prompts import (
    SYLLABUS_TOPICS_SYSTEM_PROMPT,
    SYLLABUS_TOPICS_USER_PROMPT,
    SYLLABUS_SUMMARY_SYSTEM_PROMPT,
    SYLLABUS_SUMMARY_USER_PROMPT,
)

def extract_syllabus_topics(syllabus_text: str):
    """Extract main topics from a syllabus using GPT-4o."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYLLABUS_TOPICS_SYSTEM_PROMPT},
                {"role": "user", "content": SYLLABUS_TOPICS_USER_PROMPT.format(syllabus_text=syllabus_text[:4000])},
            ]
        )
        topics = response.choices[0].message.content.split("\n")
        return [topic.strip() for topic in topics if topic.strip()]
    except Exception as e:
        raise RuntimeError(f"Error extracting syllabus topics: {str(e)}")

def generate_syllabus_summary(book_text: str, topics: list, summary_type: str):
    """Generate a structured summary for syllabus topics using GPT-4o."""
    summaries = []
    lines = "5 lines" if summary_type == "short" else "detailed explanation"
    for topic in topics:
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYLLABUS_SUMMARY_SYSTEM_PROMPT},
                    {"role": "user", "content": SYLLABUS_SUMMARY_USER_PROMPT.format(
                        topic=topic,
                        lines=lines,
                        book_text=book_text[:4000]
                    )}
                ]
            )
            summaries.append({"topic": topic, "summary": response.choices[0].message.content.strip()})
        except Exception as e:
            raise RuntimeError(f"Error generating summary for '{topic}': {str(e)}")
    return summaries
