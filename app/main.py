from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse, JSONResponse
from app.auth.auth import router as AuthRouter
from app.account.user import router as AccountRouter
from app.todos.todo import router as TodoRouter
from app.database.services import is_db_a_connected
from app.middlewares.cors import cors_middleware

app = FastAPI(title="GOAT ToDo API", version="0.0.1")
cors_middleware(app)
app.include_router(AuthRouter)
app.include_router(AccountRouter)
app.include_router(TodoRouter)


@app.get("/")
def root():
    """root alwayesnredirects to sweagger ui"""
    return RedirectResponse("/docs")


@app.get("/health")
def health():
    db_a_status = is_db_a_connected()

    if not db_a_status:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    return JSONResponse(
        {
            "API": "up",
            "DB_A_Status": db_a_status,
        }
    )
