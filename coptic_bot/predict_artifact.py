import torch
from torchvision import models, transforms
from PIL import Image
import json

# Paths
MODEL_PATH = "artifact_classifier.pth"
CLASSES_PATH = "artifact_classes.json"

# Load class names
with open(CLASSES_PATH, "r") as f:
    class_names = json.load(f)

# Load model
model = models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, len(class_names))  # same output size
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
model.eval()

# Transform for input image
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Prediction function
def predict_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = torch.max(outputs, 1)
        class_idx = predicted.item()
        class_name = class_names[class_idx]
    
    return class_name

# Example usage
if __name__ == "__main__":
    img_path = "test3.jpg"  # 👈 Replace with your test image
    prediction = predict_image(img_path)
    print(f"Predicted artifact class: {prediction}")
