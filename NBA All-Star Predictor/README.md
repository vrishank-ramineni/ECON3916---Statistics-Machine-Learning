# NBA All-Star Predictor 🏀

Predicting NBA All-Star selection from regular-season per-game statistics using machine learning.

**ECON 3916: ML Prediction Project — Spring 2026**

## Live Dashboard

🔗 **[Streamlit App]([https://your-app-name.streamlit.app](http://localhost:8501/))** *(update with your deployed URL)*

## Project Overview

**Prediction Question:** Can we predict whether an NBA player will be selected as an All-Star based on their regular-season per-game statistics?

**Stakeholder:** A sports media company (e.g., ESPN, The Ringer) deciding which borderline players to feature in pre-All-Star coverage and prediction articles.

**Key Result:** The Random Forest model achieved the best F1 score (0.704) with 69.1% precision and 71.7% recall on a held-out test set, using 13 per-game statistical features across 10 NBA seasons (2014-15 to 2023-24).

> ⚠️ **Prediction, not causation.** This model predicts All-Star selection from stats — it does not claim that changing any stat causes selection.

## Repository Structure

```
├── app.py                     # Streamlit dashboard
├── requirements.txt           # Python dependencies (pinned versions)
├── model_artifacts.pkl        # Trained models, scaler, feature list
├── nba_allstar_dataset.csv    # Full dataset (10 seasons, 4,255 player-seasons)
├── current_season_stats.csv   # Most recent season for player lookup
├── notebooks/
│   └── analysis.ipynb         # Full analysis pipeline (EDA + modeling)
├── README.md                  # This file
```

## Reproducibility

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/nba-allstar-predictor.git
cd nba-allstar-predictor
```

### 2. Set up the environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### 3. Data acquisition

The dataset is sourced from Kaggle: [NBA/ABA/BAA Stats](https://www.kaggle.com/datasets/sumitrodatta/nba-aba-baa-stats). To reproduce from scratch:

```python
import kagglehub
path = kagglehub.dataset_download("sumitrodatta/nba-aba-baa-stats")
```

The pre-processed CSVs (`nba_allstar_dataset.csv` and `current_season_stats.csv`) are included in this repo.

### 4. Run the notebook

Open `notebooks/analysis.ipynb` in Google Colab or Jupyter and run all cells. The notebook:
- Loads and cleans the Kaggle dataset
- Creates the All-Star label by merging with `All-Star Selections.csv`
- Runs EDA with 4 visualizations
- Trains 3 models (Logistic Regression, Random Forest, Gradient Boosting) with 5-fold CV and GridSearchCV
- Evaluates on a held-out test set with bootstrap confidence intervals
- Saves model artifacts for the Streamlit app

### 5. Launch Streamlit locally

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

## Models

| Model | Accuracy | Precision | Recall | F1 | AUC-ROC |
|-------|----------|-----------|--------|-----|---------|
| Logistic Regression | 0.946 | 0.539 | 0.906 | 0.676 | 0.984 |
| **Random Forest** | **0.962** | **0.691** | **0.717** | **0.704** | 0.977 |
| Gradient Boosting | 0.959 | 0.737 | 0.528 | 0.615 | 0.977 |

All models use `random_state=42` for reproducibility. Class imbalance (~6.3% All-Stars) is addressed via `class_weight='balanced'`.

## Data

- **Source:** [Kaggle — NBA/ABA/BAA Stats](https://www.kaggle.com/datasets/sumitrodatta/nba-aba-baa-stats)
- **Seasons:** 2014-15 through 2023-24 (10 seasons)
- **Observations:** 4,255 player-seasons (minimum 20 games played)
- **Target:** Binary — All-Star (1) or not (0)
- **Features:** 13 per-game statistics (PTS, AST, TRB, STL, BLK, MP, FG%, 3P%, FT%, TOV, Age, G, GS)

## Tech Stack

Python 3.10+ · pandas · scikit-learn · Streamlit · Plotly · NumPy
