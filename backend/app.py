from fastapi import FastAPI
from pydantic import BaseModel
from predict import predict

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/predict")
def predict_mood(input: TextInput):
    result = predict(input.text)
    return result

@app.get("/")
def root():
    return {"status": "ok", "message": "Moodify REST API running"}
