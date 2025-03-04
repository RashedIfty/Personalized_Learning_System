# Personalized Learning System

## Overview
The **Personalized Learning System** is a FastAPI-based application designed to help users enhance their learning experience by leveraging AI. Users can upload PDFs (books, syllabi, question papers) and then perform various operations powered by OpenAI’s GPT-4o and other AI tools, such as:

- **PDF Upload & Processing:** Upload books, syllabi, and question papers; extract text and generate embeddings.
- **Question Answering:** Ask questions based on a book’s content.
- **Quiz Generation:** Create multiple-choice quiz questions from book content.
- **Answer Key Generation:** Generate answers for questions extracted from uploaded question papers, using the corresponding book content.
- **Syllabus Summary:** Extract topics from syllabus PDFs and generate summaries based on book content.
- **Study Plan Creation:** Create personalized study plans from the content of uploaded books.
- **Research Paper Retrieval:** Extract keywords from a book and fetch related research papers using the Crossref API.
- **Google Search:** Perform Google searches using the Serper API.

**New Feature:**  
Authentication using JWT ensures that:
- All sensitive endpoints (except public ones like Google search) are secured.
- Every user sees only their own uploaded data.
- Data isolation is enforced through user-specific filtering on every operation.

---

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the API](#running-the-api)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
  - [Authentication Endpoints](#authentication-endpoints)
  - [PDF Upload & Processing](#pdf-upload--processing)
  - [Question Answering](#question-answering)
  - [Quiz Generation](#quiz-generation)
  - [Answer Key Generation](#answer-key-generation)
  - [Syllabus Summary](#syllabus-summary)
  - [Study Plan](#study-plan)
  - [Research Papers Retrieval](#research-papers-retrieval)
  - [Google Search](#google-search)
- [Database Structure](#database-structure)
- [Environment Variables](#environment-variables)
- [Folder Structure](#folder-structure)
- [Future Improvements](#future-improvements)
- [License](#license)
- [Contact](#contact)

---

## Project Structure
```
D:.
│   .env
│   database.db
│   main.py
│   README.md
│   __init__.py
│
├───app
│   ├───api
│   │   ├───answer_key_generation.py
│   │   ├───google_search.py            # Public endpoint (no auth)
│   │   ├───question_answering.py
│   │   ├───quiz_generation.py
│   │   ├───research_papers.py
│   │   ├───study_plan.py
│   │   ├───syllabus_summary.py
│   │   └───auth_endpoints.py           # Contains /register & /login endpoints
│   ├───auth                            # JWT utilities and user extraction dependency
│   │   └───auth.py
│   ├───core
│   │   ├───config.py
│   │   ├───database.py
│   │   └───embeddings.py
│   ├───db
│   │   └───crud
│   │       ├───answer_key_crud.py
│   │       ├───pdf_crud.py
│   │       ├───question_answering_crud.py
│   │       ├───quiz_crud.py
│   │       ├───research_crud.py
│   │       ├───study_plan_crud.py
│   │       └───syllabus_crud.py
│   ├───models
│   │   ├───book.py
│   │   ├───history.py
│   │   └───user.py
│   ├───schemas
│   │   ├───answer_key.py
│   │   ├───google_search.py
│   │   ├───question_answering.py
│   │   ├───quiz.py
│   │   ├───research.py
│   │   ├───study_plan.py
│   │   ├───syllabus.py
│   │   └───user.py
│   └───services
│       └───pdf_processing.py
│
├───data
│   ├───books
│   ├───embeddings
│   ├───questions
│   └───syllabus
```

---

## Installation

### Prerequisites
- Python 3.10+
- Virtual environment (recommended)
- SQLite (default database)
- OpenAI API Key
- Serper API Key (for Google search feature)

### Setup
1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file in the root directory and add:
     ```ini
     OPENAI_API_KEY=your_openai_api_key
     SERPER_API_KEY=your_serper_api_key
     DATABASE_URL=sqlite:///./database.db
     JWT_SECRET_KEY=your_jwt_secret_key   # Recommended for production
     ```

5. **Initialize the database**
   ```bash
   python -c "from app.core.database import init_db; init_db()"
   ```

---

## Running the API
To start the FastAPI server, run:
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

---

## Authentication
- **Endpoints:**  
  - `POST /api/auth/register` → Register a new user  
  - `POST /api/auth/login` → Log in and receive a JWT token

- **Usage:**  
  Include the JWT token in the Authorization header (e.g., `Bearer <token>`) for all endpoints that require authentication. This ensures that every user sees only their own data.

---

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/register` → Create a new account.
- `POST /api/auth/login` → Obtain a JWT token for authenticated sessions.

### PDF Upload & Processing
- `POST /api/pdf/upload_pdf` → Upload a book PDF and process its text and embeddings.
- `GET /api/pdf/list_books` → List all books uploaded by the current user.

### Question Answering
- `POST /api/qa/ask` → Ask questions based on a book’s content (only your own books are accessible).
- `GET /api/qa/history` → Retrieve your past queries and responses.

### Quiz Generation
- `POST /api/quiz/generate` → Generate quiz questions from a selected book (restricted to your own uploads).

### Answer Key Generation
- `POST /api/answer_key/upload_question_paper` → Upload a question paper PDF (stored uniquely per user).
- `POST /api/answer_key/generate_answers` → Generate answers for questions extracted from your question paper using the book’s content.

### Syllabus Summary
- `POST /api/syllabus/upload_syllabus` → Upload a syllabus PDF and extract topics.
- `POST /api/syllabus/summarize` → Generate summaries for the syllabus topics using a selected book.

### Study Plan
- `POST /api/study_plan/generate` → Generate a personalized study plan from a book.

### Research Papers Retrieval
- `GET /api/research/keywords` → Extract keywords from a book.
- `POST /api/research/search` → Fetch related research papers based on a query or extracted keywords.

### Google Search
- `POST /api/search` → Perform a Google search using the Serper API (public endpoint).

---

## Database Structure

### Tables
- **books:** Stores uploaded books, including filename, text content, embeddings, upload timestamp, and `user_id` for data isolation.
- **query_history:** Logs user queries and responses.
- **users:** Stores user credentials and roles for authentication.

---

## Environment Variables

| Variable          | Description                                      |
|-------------------|--------------------------------------------------|
| OPENAI_API_KEY    | API key for OpenAI GPT-4o                        |
| SERPER_API_KEY    | API key for Serper Google Search                 |
| DATABASE_URL      | SQLite database connection URL                   |
| JWT_SECRET_KEY    | Secret key for JWT token generation (production) |

---

## Folder Structure

```
D:.
│   .env
│   database.db
│   main.py
│   README.md
│   __init__.py
│
├───app
│   ├───api             # All API endpoints, including authentication endpoints
│   ├───auth            # JWT authentication utilities
│   ├───core            # Configuration and database management
│   ├───db              # CRUD operations, organized per feature
│   ├───models          # Database models (books, users, history)
│   ├───schemas         # Pydantic models for request/response validation
│   └───services        # Service modules (e.g., PDF processing)
│
├───data                # Storage for uploaded PDFs and derived data
│   ├───books
│   ├───embeddings
│   ├───questions
│   └───syllabus
```

---

## Future Improvements
- **Authentication & Security:**  
  Enhance token management, add refresh tokens, and integrate OAuth providers.
- **Database Scalability:**  
  Migrate from SQLite to PostgreSQL or MySQL for production.
- **Enhanced PDF Processing:**  
  Integrate OCR for scanned documents.
- **Analytics & Logging:**  
  Implement better logging, monitoring, and analytics of user queries.
- **UI/Frontend Integration:**  
  Develop a frontend to interact with the API more seamlessly.

---
