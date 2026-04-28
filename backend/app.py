import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Now keep your other imports...
from flask import Flask, request, jsonify
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from efficientnet_pytorch import EfficientNet
from facenet_pytorch import MTCNN
import io

app = Flask(__name__)
CORS(app)  # Allows React to talk to Flask

# --- Model Setup ---
class DeepFakeGuardModel(nn.Module):
    def __init__(self):
        super(DeepFakeGuardModel, self).__init__()
        self.backbone = EfficientNet.from_pretrained('efficientnet-b0')
        num_ftrs = self.backbone._fc.in_features
        self.backbone._fc = nn.Sequential(nn.Linear(num_ftrs, 1), nn.Sigmoid())

    def forward(self, x): return self.backbone(x)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = DeepFakeGuardModel().to(device)
model.load_state_dict(torch.load('DeepFakeGuard_v1.pth', map_location=device))
model.eval()

mtcnn = MTCNN(image_size=224, margin=20, device=device)
stats = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    img = Image.open(file.stream).convert('RGB')
    
    face = mtcnn(img)
    if face is None:
        return jsonify({'error': 'No face detected'}), 400

    face_tensor = stats(face).unsqueeze(0).to(device)
    with torch.no_grad():
        prob = model(face_tensor).item()

    label = "AI-GENERATED" if prob > 0.5 else "REAL HUMAN"
    confidence = prob if prob > 0.5 else (1 - prob)

    return jsonify({
        'verdict': label,
        'confidence': round(confidence * 100, 2)
    })

if __name__ == '__main__':
    app.run(port=5000)