# Expense Tracker API

A FastAPI-based backend for tracking expenses and managing budgets, using MongoDB (Beanie ODM) for data storage.

## Features

- Create, retrieve, and manage expenses
- MongoDB backend with Beanie ODM
- Pydantic models for validation
- OpenAPI docs (`/docs`) and ReDoc (`/redoc`)
- Environment-based configuration

## Project Structure

fastapi-expense-tracker/
├── src/
│   ├── app/
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schema.py
│   └── main.py
├── .env
├── .gitignore
└── README.md

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/lodyne/fastapi-expense-tracker.git
   cd fastapi-expense-tracker
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**

   Create a `.env` file in the project root:

   ```env
   MONGO_URL=db_url
   MONGO_DB_NAME=db_name
   MONGO_COLLECTION_NAME=db_collection_name
   ```

5. **Run MongoDB locally** (if not already running):

   ```bash
   mongod
   ```

6. **Run the API:**

   ```bash
   # If main.py is in src/, use:
   PYTHONPATH=src uvicorn main:app --reload
   ```

   Or use your alias if set:

   ```bash
   uvrun
   ```

## API Documentation

- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## License

MIT License

---

**Author:** Lodger Mtui  
**Contact:**
