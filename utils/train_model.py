import os
import joblib
from sklearn import svm
from deepface import DeepFace

embeddings = []
labels = []

dir = 'faces/known'

print("Creando embeddings")

for person in os.listdir(dir):

    face_dir = os.path.join(dir, person)

    for file in os.listdir(face_dir):

        path = os.path.join(face_dir, file)

        try:

            embedding = DeepFace.represent(
                img_path=path,
                model_name="Facenet",
                enforce_detection=False
            )[0]["embedding"]

            embeddings.append(embedding)
            labels.append(person)

            print(f"Procesado: {file}")

        except Exception as e:
            print(e)

print("Embeddings:", len(embeddings))
print("Labels:", len(labels))

print("Entrenando modelo")

model = svm.SVC(
    kernel='linear',
    probability=True
)

model.fit(embeddings, labels)

os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/svm_model.pkl")
joblib.dump(embeddings, "model/embeddings.pkl")
joblib.dump(labels, "model/labels.pkl")

print("Modelo guardado")