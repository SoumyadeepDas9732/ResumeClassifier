import pandas as pd
import re
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

# --------------------------
# LOAD DATASET
# --------------------------

df = pd.read_csv(
    "dataset/UpdatedResumeDataSet.csv"
)

print("Dataset Loaded")
print(df.head())

# --------------------------
# CLEAN TEXT
# --------------------------

def clean_text(text):

    text = re.sub(r'http\S+', '', str(text))
    text = re.sub(r'[^a-zA-Z ]', ' ', text)

    text = text.lower()

    return text


df["Resume"] = df["Resume"].apply(
    clean_text
)

# --------------------------
# ENCODE CATEGORY
# --------------------------

encoder = LabelEncoder()

df["Category"] = encoder.fit_transform(
    df["Category"]
)

# --------------------------
# TF-IDF
# --------------------------

tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X = tfidf.fit_transform(
    df["Resume"]
)

y = df["Category"]

# --------------------------
# TRAIN TEST SPLIT
# --------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# --------------------------
# MODEL
# --------------------------

model = LogisticRegression(
    max_iter=2000
)

model.fit(
    X_train,
    y_train
)

# --------------------------
# TEST MODEL
# --------------------------

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print()
print("Accuracy:", accuracy)

print()
print(classification_report(
    y_test,
    predictions
))

# --------------------------
# SAVE MODEL
# --------------------------

joblib.dump(
    model,
    "models/model.pkl"
)

joblib.dump(
    tfidf,
    "models/tfidf.pkl"
)

joblib.dump(
    encoder,
    "models/encoder.pkl"
)

print()
print("Model Saved Successfully")