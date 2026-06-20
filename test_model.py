import joblib

model = joblib.load(
    "models/model.pkl"
)

tfidf = joblib.load(
    "models/tfidf.pkl"
)

encoder = joblib.load(
    "models/encoder.pkl"
)

sample_resume = """

Python
Machine Learning
Deep Learning
TensorFlow
SQL
Data Analysis

"""

vector = tfidf.transform(
    [sample_resume]
)

prediction = model.predict(
    vector
)

role = encoder.inverse_transform(
    prediction
)

print("Predicted Role:")
print(role[0])