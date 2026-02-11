# 🍽️ Food Recipe Recommendation System (ML + Flask)

A personalized **food recipe recommendation system** built with machine learning that suggests recipes based on:

- Ingredients the user has  
- Dietary goals (weight loss, bodybuilding, diabetic, etc.)  
- Cooking time and difficulty  
- Nutritional preferences  

The system combines **multi-label classification (Random Forest)** with **content-based ranking**, delivered through a **Flask web application**.

---

## 🎯 Key Features

- Web scraping of ~3,100 recipes from **Jamie Oliver**
- Robust data cleaning & feature engineering  
- Creation of **9 diet labels** (multi-label classification)  
- **Random Forest** model with hyperparameter tuning  
- Strong performance (F1-macro ≈ **0.93**)  
- Hybrid recommender system:
  - Step 1: ML filtering by diet  
  - Step 2: Content-based scoring + ranking  
- Interactive **Flask web interface**

---

## 📁 Project Structure


---

## 📊 Dataset

**Source:** Jamie Oliver website (crawled with Selenium)  
**Size:** ~3,120 recipes  

Collected fields:
- Dish name  
- Cook time  
- Difficulty  
- Full ingredient list  
- Method steps  
- Nutrition facts  
- Recipe URL  

### Data Cleaning Highlights

- Recovered missing dish names from URLs  
- Standardized incorrect “Difficulty” values  
- Split JSON nutrition into separate columns  
- Converted **Cook Time → minutes** and binned into groups  
- Extracted **Main Ingredient from URL**  
- Built binary matrix of sub-ingredients using:
  - normalization  
  - stopword filtering  
  - singular/plural merging  
  - `MultiLabelBinarizer`

---

## 🧑‍🍳 User (Diet) Labels — 9 Targets

Each recipe may belong to **multiple groups**:

| Label | Rule (simplified) |
|---|---|
| **Low Carb** | Carbs ≤ 20g & Fat > 10g |
| **Vegetarian** | Plant-based ingredients only |
| **Weight Loss** | Low calories + high fibre/protein |
| **Bodybuilder** | High protein + moderate carbs/fat |
| **Diabetic** | Low sugar + high fibre |
| **Clean Eating** | Contains fresh whole foods |
| **Hypertension** | Low salt + low saturated fat |
| **Heart Healthy** | Limits on fat/sugar + good fats |
| **None** | Does not fit other groups |

> ⚠️ Labels are imbalanced → handled with `class_weight="balanced"`.

---

## 🤖 Model: Random Forest (Multi-Label)

### Features used
- One-hot: Difficulty, Main Ingredient, Cook Time group  
- Numeric: Calories, Fat, Carbs, Protein, Fibre, Salt, etc.  
- Binary sub-ingredients (≈ 700+ features)

### Training Strategy
- 60% train / 20% validation / 20% test  
- 5-fold cross-validation  
- GridSearch + RandomizedSearch

### Best Hyperparameters

n_estimators = 500
max_depth = 35
min_samples_split = 5
min_samples_leaf = 1
max_features = None
### Performance (Test Set)

| Metric | Value |
|---|---|
| Hamming Loss | 0.026 |
| Subset Accuracy | 0.795 |
| F1-macro | 0.928 |
| F1-micro | 0.919 |

✔ Label-shuffle sanity check confirmed **no data leakage**.

---

## 🔄 Recommendation Pipeline

### Step 1 — ML Filtering  
User selects a diet → model predicts probability per recipe → keep those with `p ≥ 0.5`.

### Step 2 — Content-Based Scoring  
Each remaining recipe gets a weighted score based on:

- Cosine similarity to user profile  
- Main ingredient match  
- Sub-ingredient match  
- Cooking time fit  
- Difficulty fit  
- Calorie compatibility  

### Step 3 — Ranking  
Top **15 diverse recipes** are returned.

---

## 🌐 Flask Web App

Run locally:

```bash
pip install -r requirements.txt
python app/app.py


## 📦 Dependencies
pandas
numpy
scikit-learn
matplotlib
seaborn
joblib
flask
selenium
