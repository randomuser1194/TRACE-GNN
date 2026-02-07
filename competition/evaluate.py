import pandas as pd
import sys
from sklearn.metrics import f1_score

def main(pred_path, label_path, score_path):
    labels = pd.read_csv(label_path).sort_values("id")
    preds = pd.read_csv(pred_path).sort_values("id")
    
    mask = labels['label'].isin([0, 1]).values
    
    labels = labels[mask]
    labels.rename(columns={'label': 'y_true'}, inplace=True)
    
    preds = preds[mask]

    merged = labels.merge(preds, on="id", how="inner")
    if len(merged) != len(labels):
        raise ValueError("ID mismatch between predictions and labels")

    score = f1_score(merged["y_true"], merged["y_pred"], average="macro")
    print(f"SCORE={score:.8f}")
    
    with open(score_path, "w") as f:
        f.write(f"{score:.6f}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
