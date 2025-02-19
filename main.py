import os
import webbrowser
import threading
from functools import wraps
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from pymongo import MongoClient
from dotenv import load_dotenv
import bcrypt
import logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace.status import Status, StatusCode

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[logging.FileHandler('app.log'), logging.StreamHandler()])
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

def trace_and_log(span_name):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(span_name) as span:
                try:
                    result = await func(*args, **kwargs)
                    span.set_status(Status(StatusCode.OK))
                    logger.info(f"{span_name} completed successfully")
                    return result
                except HTTPException as e:
                    span.set_status(Status(StatusCode.ERROR))
                    span.set_attribute("error.type", type(e).__name__)
                    span.set_attribute("error.message", str(e))
                    logger.error(f"{span_name} failed: {e.detail}")
                    raise
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR))
                    span.set_attribute("error.type", type(e).__name__)
                    span.set_attribute("error.message", str(e))
                    logger.error(f"{span_name} failed: {str(e)}")
                    raise
        return wrapper
    return decorator

def setup_telemetry():
    resource = Resource.create({"service.name": "user-registration-service"})
    provider = TracerProvider(resource=resource)
    
    try:
        collector_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")
        otlp_exporter = OTLPSpanExporter(endpoint=collector_endpoint, insecure=True, timeout=5.0)
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    except Exception:
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    
    trace.set_tracer_provider(provider)
    return trace.get_tracer(__name__)

load_dotenv()
mongo_url = os.getenv("MONGO_URL")
if not mongo_url:
    logger.error("MongoDB URL not found")
    exit(1)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

try:
    client = MongoClient(mongo_url)
    db = client["my_database"]
    users_collection = db["users"]
except Exception as e:
    logger.error(f"MongoDB connection failed: {e}")
    exit(1)

FastAPIInstrumentor.instrument_app(app)
PymongoInstrumentor().instrument()

@app.get("/register")
@trace_and_log("serve_register_form")
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
@trace_and_log("process_registration")
async def register(email: EmailStr = Form(...), password: str = Form(...)):
    user = users_collection.find_one({"email": email})
    if not user:
        logger.error(f"Authentication failed: User with email {email} does not exist")
        raise HTTPException(status_code=400, detail="Wrong email and password combination.")
    
    if not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        logger.error(f"Authentication failed: Invalid password for user {email}")
        raise HTTPException(status_code=400, detail="Wrong email and password combination.")
    
    logger.info(f"User {email} successfully authenticated")
    return {"message": "User registered successfully"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error: {str(exc)}")
    return {"detail": "Internal Server Error"}

def open_browser():
    webbrowser.open("http://127.0.0.1:8000/register")

if __name__ == "__main__":
    import uvicorn
    threading.Timer(1.5, open_browser).start()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")