#### DeepFake Guard
A full-stack AI application that detects synthetic faces using Deep Learning.

##  Features
- **MTCNN**: For precise face extraction and alignment.
- **EfficientNet-B0**: High-accuracy deep learning model for artifact detection.
- **React Frontend**: Modern, dark-mode UI for seamless image analysis.
- **Flask API**: Robust backend to handle model inference.

## Setup
### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. `python app.py`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Model Performance
- **Training Dataset**: Celeb-DF
- **Detection Target**: GANs (StyleGAN), FaceSwaps.
