import torch
import torch.backends.cudnn as cudnn
from torchvision import transforms
import matplotlib.pyplot as plt
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

cudnn.benchmark = True
plt.ion()

weights_path = "data/models/BestModel.pth"
class_names = ['Plate1x1(3024)', 'Plate1x10(4477)', 'Plate1x12(60479)', 'Plate1x2(3023)', 'Plate1x3(3623)', 'Plate1x4(3710)', 'Plate1x5(78329)', 'Plate1x6(3666)', 'Plate1x8(3460)', 'Plate2x10(3832)', 'Plate2x12(2445)', 'Plate2x14(91988)', 'Plate2x16(4282)', 'Plate2x2(3022)', 'Plate2x2Corner(2420)', 'Plate2x3(3021)', 'Plate2x4(3020)', 'Plate2x6(3795)', 'Plate2x8(3034)', 'Plate3x3(11212)', 'Plate3x3Corner(77844)', 'Plate4x10(3030)', 'Plate4x12(3029)', 'Plate4x4(3031)', 'Plate4x4Corner(2639)', 'Plate4x6(3032)', 'Plate4x8(3035)', 'Plate6x10(3033)', 'Plate6x12(3028)', 'Plate6x14(3456)', 'Plate6x16(3027)', 'Plate6x24(3026)', 'Plate6x6(3958)', 'Plate6x8(3036)', 'Plate8x16(92438)', 'Plate8x8(42534)']

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load(weights_path, map_location=device, weights_only=False)
model = model.to(device)
model.eval()

# Define the FastAPI app
app = FastAPI()

# Configure the API
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the prediction function
def predict(image: Image.Image):
    # Preprocess the image
    preprocess = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = preprocess(image).unsqueeze(0).to(device)

    print(image.shape)

    # Perform the prediction
    with torch.no_grad():
        prediction = model(image)
        probabilities = torch.nn.functional.softmax(prediction, dim=1)[0] * 100
        top3_prob, top3_index = torch.topk(probabilities, 3)
        top3_classes = [class_names[index] for index in top3_index.cpu().numpy()]
    return zip(top3_classes, top3_prob)

# Define the API endpoint
@app.post("/predict")
async def predict_api(file: UploadFile = File(...)):
    image = Image.open(file.file).convert('RGB')
    predictions = predict(image)
    return {"predictions": [{"label": label, "probability": probability.item()} for label, probability in predictions]}