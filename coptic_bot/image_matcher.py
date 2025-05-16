import os
import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer
import torchvision.transforms as transforms
import torch

model = SentenceTransformer("clip-ViT-B-32")
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

def get_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    embedding = model.encode([image], convert_to_tensor=True)  # list of PIL.Image
    return embedding

def match_artifact_by_image(image_path, artifacts):
    query_embedding = get_embedding(image_path)
    best_match = None
    best_score = -1

    for artifact in artifacts:
        artifact_path = artifact.get("image_path")
        if artifact_path and os.path.exists(artifact_path):
            try:
                db_embedding = get_embedding(artifact_path)
                score = torch.cosine_similarity(query_embedding, db_embedding).item()
                if score > best_score:
                    best_score = score
                    best_match = artifact
            except:
                continue

    return {"match": best_match, "score": best_score}
