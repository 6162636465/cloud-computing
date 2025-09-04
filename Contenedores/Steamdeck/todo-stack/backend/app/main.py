import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Boolean, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://todo:todo@db:5432/todo_db")
API_PORT = int(os.getenv("API_PORT", "8000"))
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoIn(BaseModel):
    title: str
    done: bool = False

class TodoOut(TodoIn):
    id: int

@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}

@app.get("/todos", response_model=List[TodoOut])
def list_todos(db: Session = Depends(get_db)):
    return db.query(Todo).order_by(Todo.id.desc()).all()

@app.post("/todos", response_model=TodoOut)
def create(todo: TodoIn, db: Session = Depends(get_db)):
    obj = Todo(title=todo.title, done=todo.done)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.put("/todos/{todo_id}", response_model=TodoOut)
def update(todo_id: int, todo: TodoIn, db: Session = Depends(get_db)):
    obj = db.query(Todo).get(todo_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    obj.title, obj.done = todo.title, todo.done
    db.commit(); db.refresh(obj)
    return obj

@app.delete("/todos/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    obj = db.query(Todo).get(todo_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(obj); db.commit()
    return {"deleted": True}
