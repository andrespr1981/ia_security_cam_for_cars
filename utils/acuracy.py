import os
import joblib
from sklearn.metrics import accuracy_score, classification_report
from deepface import DeepFace

model = joblib.load("model/svm_model.pkl")

X_test = []
y_test = []

test_dir = "faces/test"

print("Creando embeddings")

for person in os.listdir(test_dir):

    person_dir = os.path.join(test_dir, person)

    for file in os.listdir(person_dir):

        path = os.path.join(person_dir, file)

        try:

            embedding = DeepFace.represent(
                img_path=path,
                model_name="Facenet",
                enforce_detection=False
            )[0]["embedding"]

            X_test.append(embedding)
            y_test.append(person)

            print(f"Procesado: {file}")

        except Exception as e:
            print("Error:", e)

print("Evaluando modelo")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"\nAccuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        predictions
    )
)