"""Unit tests for main.py module."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# FastAPI App Setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
