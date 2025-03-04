# --------------------------
# Prompts from answer_key_llm.py
# --------------------------

# For extract_questions_from_book function
EXTRACT_QUESTIONS_SYSTEM_PROMPT = "Extract questions from the given book."
EXTRACT_QUESTIONS_USER_PROMPT = "{book_text}"  # book_text is truncated to 4000 characters

# For generate_answers_from_book function
GENERATE_ANSWERS_SYSTEM_PROMPT = "Provide a structured and concise answer based on the book content."
GENERATE_ANSWERS_USER_PROMPT = (
    "Answer the following based on the book:\n\n{book_text}\n\nQuestion: {question}"
)


# --------------------------
# Prompts from question_answering_llm.py
# --------------------------

QUESTION_ANSWERING_SYSTEM_PROMPT = "You are an AI assistant answering questions based on a stored book. You will give answers based on the content of the book. But all of the questions will be from the question paper. Dont generate questions on your own. Questions are from question pdf and answers are from the book."    
QUESTION_ANSWERING_USER_PROMPT = (
    "Here is the book content:\n\n{book_text}\n\nQuestion: {question}"
)


# --------------------------
# Prompts from quiz_llm.py
# --------------------------

QUIZ_GENERATION_SYSTEM_PROMPT = (
    "You are an AI assistant that generates quiz questions and multiple-choice answers. There should be no prembles or introductions in the questions. Just the question and the options and the right answer."
)
QUIZ_GENERATION_USER_PROMPT = (
    "Here is a book:\n\n{book_text}\n\nGenerate {num_questions} quiz questions with multiple-choice answers."
)


# --------------------------
# Prompts from research_llm.py
# --------------------------

RESEARCH_KEYWORDS_SYSTEM_PROMPT = (
    "Extract and return the most relevant keywords from the given book text."
)
RESEARCH_KEYWORDS_USER_PROMPT = "{book_text}"  # book_text is truncated to 4000 characters


# --------------------------
# Prompts from study_plan_llm.py
# --------------------------

STUDY_PLAN_SYSTEM_PROMPT = "You are an AI assistant that generates study plans."
STUDY_PLAN_USER_PROMPT = (
    "Here is a book:\n\n{book_text}\n\nCreate a {duration}-day study plan covering the most important topics from the document."
)


# --------------------------
# Prompts from syllabus_llm.py
# --------------------------

SYLLABUS_TOPICS_SYSTEM_PROMPT = (
    "Extract and return a structured list of main topics from the given syllabus."
)
SYLLABUS_TOPICS_USER_PROMPT = "{syllabus_text}"  # syllabus_text is truncated to 4000 characters

SYLLABUS_SUMMARY_SYSTEM_PROMPT = (
    "Provide a structured and informative summary of the topic based on the book."
)
# Note: 'lines' is a placeholder that should be set to "5 lines" for short summaries or "detailed explanation" otherwise.
SYLLABUS_SUMMARY_USER_PROMPT = (
    "Summarize '{topic}' in {lines} using the book content:\n\n{book_text}"
)
