# app.py – Updated scoring system with new requirements
import json
import joblib
from pathlib import Path

import numpy as np
import pandas as pd
from flask import Flask, render_template, request, abort

# ───────────────────────────────
# 1. Load data
# ───────────────────────────────
items = pd.read_csv("data/merged_items.csv")
items.reset_index(inplace=True)
items.rename(columns={"index": "RID"}, inplace=True)

# Ép kiểu Cook Time về số (nếu cột tồn tại)
if "Cook Time" in items.columns:
    items["Cook Time"] = pd.to_numeric(
        items["Cook Time"], errors="coerce"
    ).fillna(0).astype(int)
elif "Cook Time (Minutes)" in items.columns:
    items["Cook Time (Minutes)"] = pd.to_numeric(
        items["Cook Time (Minutes)"], errors="coerce"
    ).fillna(0).astype(int)
else:
    # Tạo cột mặc định
    items["Cook Time"] = 0

# Merge image_url nếu có
img_csv = Path("data/image_url.csv")
if img_csv.exists():
    img_df = pd.read_csv(img_csv)
    if "image_url" in img_df.columns:
        items = items.merge(img_df, on="Dish Name", how="left")
    else:
        items["image_url"] = ""
else:
    items["image_url"] = ""
items["image_url"] = items["image_url"].fillna("").astype(str).replace("nan", "")

# Ép kiểu Calories
items["Calories"] = pd.to_numeric(items["Calories"], errors="coerce")
items["Calories"].fillna(items["Calories"].median(), inplace=True)

# ───────────────────────────────
# 2. Load model & feature cols
# ───────────────────────────────
model = joblib.load("models/best_randomized_search_CV.pkl")
with open("models/columns.json") as f:
    feature_cols = json.load(f)

# Add missing feature cols
for col in feature_cols:
    if col not in items.columns:
        items[col] = 0

target_cols = [
    "Weight_Loss", "Bodybuilder", "CleanEating", "Diabetic",
    "Hypertension", "Heart-Healthy Diet", "Vegetarian", "Low_Carb", "None"
]

X_full = items[feature_cols]
probs = model.predict_proba(X_full)
prob_df = pd.DataFrame({t: probs[i][:, 1] for i, t in enumerate(target_cols)})

# ───────────────────────────────
# 3. Form choices
# ───────────────────────────────
main_choices = sorted(items["Main Ingredient"].str.lower().unique())
sub_cols     = items.columns[16:690]
sub_choices  = sorted([c for c in sub_cols if items[c].sum() > 20])

CAL_BUCKETS   = [(100, 299), (300, 499), (500, 699), (700, 899), (900, 99999)]
DEFAULT_BUCKET = len(CAL_BUCKETS) - 1

# ───────────────────────────────
# 4. Flask app
# ───────────────────────────────
app = Flask(__name__)

@app.route("/")
def index():
    return render_template(
        "index.html",
        mains=main_choices,
        subs=sub_choices,
        cal_ranges=CAL_BUCKETS
    )

@app.route("/recommend", methods=["POST"])
def recommend():
    f = request.form

    # 1. Main ingredient
    main_inp = f.get("main", "").lower().strip()

    # 2. Additional ingredients: tách từ chuỗi comma‐separated trong <input name="sub">
    sub_raw = f.get("sub", "")            # => ví dụ "tomato,garlic,basil"
    sub_inp = [s.strip().lower() for s in sub_raw.split(",") if s.strip()]
    # DEBUG: in thử ra console
    print("DEBUG sub_raw:", sub_raw)
    print("DEBUG sub_inp list:", sub_inp)

    # 3. Cook time
    try:
        time_inp = int(f.get("time", 0))
    except ValueError:
        time_inp = 0

    # 4. Skill / Diet / Calories
    skill_inp = f.get("skill", "").upper()
    diet_inp  = f.get("diet", "none")
    try:
        cal_idx = int(f.get("cal_range", 0))
    except ValueError:
        cal_idx = 0

    results = []
    for idx, row in items.iterrows():
        score = 0.0  # Start with 0 instead of 10

        # 1. Main ingredient scoring - 140 points if match, 0 if not
        if row["Main Ingredient"].lower() == main_inp:
            score += 140

        # 2. Sub ingredients scoring - 30 points per match
        match_count = sum(1 for ing in sub_inp if row.get(ing, 0) == 1)
        score += 30 * match_count

        # 3. Cook time scoring (updated logic)
        cook_time = row.get("Cook Time", 0)
        if cook_time == 0 and "Cook Time (Minutes)" in row:
            cook_time = row["Cook Time (Minutes)"]
        
        time_diff = abs(cook_time - time_inp)
        
        if time_inp < 75:
            # User input under 75 mins
            if time_diff <= 30:
                score += 60  # Within 30 minutes difference
            else:
                score -= 50  # Beyond 30 minutes difference
        else:
            # User input 75+ mins
            if time_diff <= 45:
                score += 40  # Within 45 minutes difference
            else:
                # Beyond 45 minutes, subtract 15 for each additional 45-min block
                excess_blocks = (time_diff - 45) // 45 + 1
                score -= 15 * excess_blocks

        # 4. Skill level scoring - 60 points if match, -40 if not
        if row["Difficulty"].upper() == skill_inp:
            score += 60
        else:
            score -= 40

        # 5. Diet preference scoring - 90 points if match, 0 if not
        if diet_inp != "none" and row.get(diet_inp, 0) == 1:
            score += 90

        # 6. Calories bucket scoring - 50 points if match, -20 per bucket difference
        cal_val = row["Calories"]
        try:
            bucket = next(i for i, (lo, hi) in enumerate(CAL_BUCKETS) if lo <= cal_val <= hi)
        except StopIteration:
            bucket = DEFAULT_BUCKET
        
        if bucket == cal_idx:
            score += 50
        else:
            bucket_diff = abs(bucket - cal_idx)
            score -= 20 * bucket_diff

        # 7. Model probability bonus (keep existing logic)
        if diet_inp != "none":
            score += 10 * prob_df.loc[idx, diet_inp]

        # 8. Default case bonus - add 10 points for any other scenarios
        score += 10

        # image URL
        img_url = row.get("image_url", "") or ""
        if pd.isna(img_url) or str(img_url).lower() in ["nan", "none", ""]:
            img_url = ""

        results.append({
            "rid":   int(row["RID"]),
            "name":  row["Dish Name"],
            "score": round(score, 2),
            "time":  cook_time,
            "cal":   int(cal_val),
            "image": img_url
        })

    top15 = sorted(results, key=lambda d: d["score"], reverse=True)[:15]
    return render_template("results.html", dishes=top15)

@app.route("/recipe/<int:rid>")
def recipe(rid):
    if rid not in items["RID"].values:
        abort(404)
    r = items.loc[items["RID"] == rid].iloc[0]

    img_url = r.get("image_url", "") or ""
    if pd.isna(img_url) or str(img_url).lower() in ["nan", "none"]:
        img_url = ""

    r_dict = r.to_dict()
    r_dict["image_url"] = img_url

    return render_template(
        "detail.html",
        r=r_dict,
        ings=r["Ingredients"].split("|"),
        steps=r["Method"].split("|")
    )

if __name__ == "__main__":
    app.run(debug=True)