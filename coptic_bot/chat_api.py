from dotenv import load_dotenv
load_dotenv()

import os
os.environ["HF_HOME"] = "D:/huggingface_cache"

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import FARMReader, EmbeddingRetriever
from haystack.pipelines import ExtractiveQAPipeline
from image_matcher import match_artifact_by_image
from database import load_artifacts
from scripts.export_artifacts import export_artifacts_from_db  # 👈 NEW IMPORT
import uvicorn
import shutil
from fastapi.responses import RedirectResponse
from classifier import classify_artifact
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from scripts.export_artifacts import export_artifacts_from_db

scheduler = BackgroundScheduler()
scheduler.add_job(export_artifacts_from_db, 'interval', minutes=30)  # Every 30 mins
scheduler.start()

current_artifact_context: Optional[dict] = None  # 👈 holds current artifact details



app = FastAPI()

# @app.get("/", include_in_schema=False)
# async def root_redirect():
#     return RedirectResponse(url="/chat")
# Haystack setup
document_store = FAISSDocumentStore(
    faiss_index_path="models/faiss_index.faiss",
    faiss_config_path="models/faiss_index.json"
)
retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    use_gpu=True
)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
qa_pipeline = ExtractiveQAPipeline(reader=reader, retriever=retriever)

# Load artifacts from JSON
artifacts_db = load_artifacts("data/artifacts.json")

# Models
class Question(BaseModel):
    query: str

# Routes
@app.post("/ask")
def ask_question(data: Question):
    query = data.query.strip()

    # If an artifact is selected, use contextual Q&A
    if current_artifact_context:
        context_text = f"""
        Artifact Name: {current_artifact_context.get('name', '')}
        Description: {current_artifact_context.get('description', '')}
        Period: {current_artifact_context.get('period', '')}
        """

        combined_query = f"{context_text}\n\nQuestion: {query}"
    else:
        # General question
        combined_query = query

    prediction = qa_pipeline.run(query=combined_query, params={"Retriever": {"top_k": 3}, "Reader": {"top_k": 2}})
    answers = prediction.get("answers", [])

    response = [{
        "answer": a.answer,
        "context": a.context,
        "score": a.score,
        "source": a.meta.get("source_file", "unknown")
    } for a in answers]

    result = {
        "answers": response
    }

    # Include artifact image if available
    if current_artifact_context:
        image_path = current_artifact_context.get("image_path")
        image_url = f"/{image_path}" if image_path else None

        result["artifact"] = {
            "name": current_artifact_context.get("name"),
            "image_url": image_url,
        }

    return result




@app.post("/identify-artifact")
async def identify_artifact(file: UploadFile = File(...)):
    global current_artifact_context

    os.makedirs("temp", exist_ok=True)
    filepath = f"temp/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    predicted_class = classify_artifact(filepath)

    artifact_info = next((a for a in artifacts_db if a["name"] == predicted_class), None)

    current_artifact_context = artifact_info  # 👈 set global context

    if artifact_info:
        return {
            "predicted_class": predicted_class,
            "artifact_info": artifact_info
        }
    else:
        return {
            "predicted_class": predicted_class,
            "artifact_info": None,
            "message": "Artifact details not found in database."
        }



@app.get("/sync-artifacts")  # 👈 NEW ROUTE
def sync_artifacts():
    result = export_artifacts_from_db()
    return result


@app.post("/reset-artifact")
def reset_artifact():
    global current_artifact_context
    current_artifact_context = None
    return {"message": "Artifact context has been reset."}

# Run server
if __name__ == "__main__":
    uvicorn.run("chat_api:app", host="127.0.0.1", port=8001, reload=True)
