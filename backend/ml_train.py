import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib, os

data = pd.read_csv("training_data.csv")

vector = TfidfVectorizer()
X = vector.fit_transform(data["text"])
y = data["category"]

model = MultinomialNB()
model.fit(X, y)

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/model.pkl")
joblib.dump(vector, "model/vector.pkl")

print("Model trained")
