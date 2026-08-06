# TEMP DEBUG - REMOVE AFTER RENDER INVESTIGATION
print("[startup] app.main: before FastAPI import", flush=True)
from fastapi import FastAPI
print("[startup] app.main: after FastAPI import", flush=True)

print("[startup] app.main: before CORSMiddleware import", flush=True)
from fastapi.middleware.cors import CORSMiddleware
print("[startup] app.main: after CORSMiddleware import", flush=True)

print("[startup] app.main: before app.api.routes import", flush=True)
from app.api.routes import router
print("[startup] app.main: after app.api.routes import", flush=True)

print("[startup] app.main: before FastAPI()", flush=True)
app = FastAPI(
    title="RAG PDF Q&A Bot",
    version="1.0.0",
)
print("[startup] app.main: after FastAPI()", flush=True)

print("[startup] app.main: before add_middleware", flush=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("[startup] app.main: after add_middleware", flush=True)

print("[startup] app.main: before include_router", flush=True)
app.include_router(router)
print("[startup] app.main: after include_router", flush=True)
