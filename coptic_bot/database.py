import json

def load_artifacts(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    
    artifacts = []
    for item in raw:
        artifact = {
            "id": item["id"],
            "name": item["name"],
            "description": item["description"],
            "period": item["historical_period"],
            "province": item["province"],
            "material": item["material"],
            "image_url": item["image"],
            "image_path": f"data/artifacts/{item['id']}.jpg",  # assumes local images stored by ID
            "hall": item.get("hall", {}).get("name", "")
        }
        artifacts.append(artifact)
    return artifacts
