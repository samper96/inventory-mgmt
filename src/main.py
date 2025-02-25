"""
Main Application entrypoint.

This script initializes the FastAPI application, includes API routers,
and sets up the CORS middleware and logging configuration.
"""

import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import engine, Base
from routers import products, websocket

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(asctime)s | %(name)s:%(lineno)d - %(message)s")
logger = logging.getLogger(__name__)

# FastAPI App setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Register API routers
app.include_router(products.router)
app.include_router(websocket.router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Defines the 'startup' and 'shutdown' logic.

    The logic before `yield` is executed before the server starts accepting requests.
    Logic after `yield` is executed after the server shuts down.
    """
    # ---- EXECUTED BEFORE SERVER STARTS ----
    logger.info("Starting up the Inventory Management System API...")

    # Create database tables
    Base.metadata.create_all(bind=engine)

    yield

    # --- EXECUTED AFTER SERVER SHUTS DOWN ----
    logger.info("Shutting down the Inventory Management System API...")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all exception handler for any uncaught exceptions.

    Returns a 500 response with a generic error message.
    """
    logger.error("Unhandled Exception: %s" % exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"Error details": "An unexpected error occurred on the server."},
    )


if __name__ == "__main__":
    uvicorn.run(app, "0.0.0.0", port=8000)
