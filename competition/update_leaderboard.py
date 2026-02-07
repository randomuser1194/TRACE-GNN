import sys
import os
import json
import pandas as pd
from datetime import datetime, timezone

# ---------------------------
# Inputs
# ---------------------------
score_file = sys.argv[1]      
metadata_file = sys.argv[2]   


leaderboard_csv = "../leaderboard/leaderboard.csv"

# ---------------------------
# Read score
# ---------------------------
with open(score_file, "r") as f:
    score = float(f.read().strip())

# ---------------------------
# Read metadata
# ---------------------------
with open(metadata_file, "r") as f:
    metadata = json.load(f)

team = metadata.get("team", "unknown")
run_id = metadata.get("run_id", "unknown")
type_ = metadata.get("type", "unknown")
model = metadata.get("model", "unknown")

# ---------------------------
# Current timestamp UTC
# ---------------------------
timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

# ---------------------------
# Prepare new row
# ---------------------------
new_row = {
    "timestamp_utc": timestamp,
    "team": team,
    "run_id": run_id,
    "type": type_,
    "model": model,
    "score": score
}

# ---------------------------
# Append to leaderboard.csv
# ---------------------------
if os.path.exists(leaderboard_csv):
    # Load existing leaderboard
    df = pd.read_csv(leaderboard_csv)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
else:
    # Create new leaderboard with headers
    df = pd.DataFrame([new_row])

# Save updated leaderboard
df.to_csv(leaderboard_csv, index=False)

print(f"✅ Leaderboard updated: {leaderboard_csv}")
