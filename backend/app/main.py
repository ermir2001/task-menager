from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import user, task, project, task_comment, task_status, task_priority

from app.routes.auth import router as auth_router
from app.routes.tasks import router as tasks_router
from app.routes.projects import router as projects_router
from app.routes.task_comments import router as task_comments_router
from app.routes.task_statuses import router as task_statuses_router
from app.routes.task_priorities import router as task_priorities_router
from app.routes.users import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(projects_router)
app.include_router(task_comments_router)
app.include_router(task_statuses_router)
app.include_router(task_priorities_router)
app.include_router(users_router)


@app.get("/")
def root():
    return {"message": "API działa"}