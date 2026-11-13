import os
import pickle
import numpy as np

try:
    from tensorflow import keras
    from tensorflow.keras import layers
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

MODEL_H5 = os.path.join("model", "yoga_model.h5")
MODEL_PKL = os.path.join("model", "yoga_model.pkl")
POSE_CLASSES = [
    "Mountain Pose",
    "Tree Pose",
    "Warrior Pose",
    "Triangle Pose",
    "Cobra Pose",
]


def create_synthetic_dataset():
    features = []
    labels = []

    def add_sample(values, label, count=25):
        for _ in range(count):
            noise = np.random.normal(0, 6, size=len(values))
            features.append(np.clip(np.array(values) + noise, 10, 180))
            labels.append(label)

    add_sample([170, 170, 175, 175, 170, 170, 175, 175, 175], 0)  # Mountain
    add_sample([70, 30, 90, 90, 100, 100, 80, 80, 175], 1)  # Tree
    add_sample([160, 160, 80, 80, 150, 150, 160, 160, 110], 2)  # Warrior
    add_sample([145, 145, 60, 120, 140, 140, 160, 160, 160], 3)  # Triangle
    add_sample([55, 55, 50, 50, 150, 150, 170, 170, 100], 4)  # Cobra

    return np.array(features, dtype=np.float32), np.array(labels, dtype=np.int32)


def build_model(input_shape):
    model = keras.Sequential([
        layers.Input(shape=(input_shape,)),
        layers.Dense(64, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(64, activation="relu"),
        layers.Dense(len(POSE_CLASSES), activation="softmax"),
    ])
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def train_and_save():
    x, y = create_synthetic_dataset()

    if not os.path.exists("model"):
        os.makedirs("model")

    if TENSORFLOW_AVAILABLE:
        model = build_model(x.shape[1])
        model.fit(x, y, epochs=50, batch_size=16, verbose=0)
        model.save(MODEL_H5)
        print(f"TensorFlow model trained and saved to {MODEL_H5}")
    else:
        from sklearn.neural_network import MLPClassifier

        classifier = MLPClassifier(hidden_layer_sizes=(64, 64), max_iter=500, random_state=42)
        classifier.fit(x, y)
        with open(MODEL_PKL, "wb") as model_file:
            pickle.dump(classifier, model_file)
        print(f"sklearn model trained and saved to {MODEL_PKL}")


def main():
    train_and_save()


if __name__ == "__main__":
    main()
