import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = os.path.abspath("../backend/model/moodify_model")

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

print(" Model and tokenizer loaded!")
