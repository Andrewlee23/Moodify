import pandas as pd
import glob

# Paths
GOEMOTIONS_PATHS = glob.glob("../data/goemotions_*.csv")  
KAGGLE_PATH = "../data/kaggle.csv"
OUTPUT_PATH = "../data/final_dataset.csv"


# Load Kaggle dataset

kaggle = pd.read_csv(KAGGLE_PATH, names=["text", "label"])  

kaggle_map = {
    0: "sadness",
    1: "happy",
    2: "happy",   # love -> happy
    3: "angry",
    4: "fear",
    5: "silly"    # surprise -> silly
}

kaggle["label"] = kaggle["label"].map(kaggle_map)
kaggle = kaggle[["text", "label"]]

# Load GoEmotions dataset (all 3 parts)
dfs = [pd.read_csv(path) for path in GOEMOTIONS_PATHS]
goemotions = pd.concat(dfs, ignore_index=True)
emotion_cols = goemotions.columns[11:]

go_map = {
    "angry": ["anger", "annoyance", "disapproval"],
    "happy": ["joy", "excitement", "optimism", "admiration", "love"],
    "fear": ["fear", "nervousness"],
    "sadness": ["sadness", "disappointment", "grief", "remorse"],
    "disgust": ["disgust", "embarrassment"],
    "silly": ["amusement", "curiosity", "surprise", "playful"]
}

rows = []
for _, row in goemotions.iterrows():
    text = row["text"]
    assigned = None
    for mood, cols in go_map.items():
        for col in cols:
            if col in row and row[col] == 1: 
                assigned = mood
                break
        if assigned:
            break
    if assigned:
        rows.append({"text": text, "label": assigned})

go_clean = pd.DataFrame(rows)

dataset = pd.concat([kaggle, go_clean], ignore_index=True)
dataset = dataset.dropna().sample(frac=1).reset_index(drop=True)

final_label_map = {
    "angry": 0,
    "happy": 1,
    "fear": 2,
    "sad": 3,
    "disgusted": 4,
    "silly": 5
}

dataset["label"] = dataset["label"].map(final_label_map)

dataset.to_csv(OUTPUT_PATH, index=False)

print(f"Dataset saved to {OUTPUT_PATH} with {len(dataset)} rows")
print(dataset['label'].value_counts())
print(dataset.head())