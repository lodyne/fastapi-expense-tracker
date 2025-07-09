from fastapi import FastAPI

app = FastAPI(
    title="Expense Tracker API",
    description="An API for tracking expenses and managing budgets",
    version="1.0.0",
    contact={"name": "Lodger Mtui", "email": "lodgmtui@gmail.com"},
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit/"},
    openapi_tags=[
        {"name": "expenses", "description": "Operations related to expenses"}
    ],
)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}
