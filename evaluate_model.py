"""Exploratory evaluation on tiny synthetic data. Not a production benchmark."""
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from ml_model import TRAINING_EXAMPLES, build_model

X = [text for text, label in TRAINING_EXAMPLES]
y = [label for text, label in TRAINING_EXAMPLES]
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
predictions = cross_val_predict(build_model(), X, y, cv=cv)

print("Dataset size:", len(X))
print("Exploratory 3-fold cross-validation")
print("Accuracy:", round(accuracy_score(y, predictions), 3))
print(classification_report(y, predictions, zero_division=0))
labels = ["Low information", "Needs clarification", "Ready for discovery"]
print("Label order:", labels)
print(confusion_matrix(y, predictions, labels=labels))
print("WARNING: Synthetic data and tiny sample; metrics are not evidence of real-world performance.")
