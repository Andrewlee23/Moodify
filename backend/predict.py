from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
MODEL_PATH = "model/moodify_model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

id2label = {
    0: "angry",
    1: "happy",
    2: "fear",
    3: "sad",
    4: "disgusted",
    5: "silly"
}
def predict(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    label_id = probs.argmax().item()
    return {
        "label": id2label[label_id],
        "probabilities": {id2label[i]: float(probs[0][i]) for i in range(len(id2label))}
    }
