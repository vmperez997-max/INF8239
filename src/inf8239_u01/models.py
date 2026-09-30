"""Construcción del modelo SVM para clasificación."""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def build_svm(C=1.0, kernel="rbf", gamma="scale", probability=True, random_state=42):
    """Crea un pipeline de escalado y SVM con regularización positiva."""
    if C <= 0:
        raise ValueError("C debe ser mayor que cero.")

    return Pipeline([
        ("scale", StandardScaler()),
        ("model", SVC(
            C=C,
            kernel=kernel,
            gamma=gamma,
            probability=probability,
            random_state=random_state,
        )),
    ])
