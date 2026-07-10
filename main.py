"""
PROJECT HAALU - COMPLETE END-TO-END PIPELINE
A Study of Milk Types and Their Correlation with Quality Variables
Extended with: Karnataka sampling locations, hypothesis testing, SMOTE, cross-validation.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import pearsonr, f_oneway, ttest_ind
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

np.random.seed(42)

# STEP 1: DATASET CONSTRUCTION (Report Sec 2.1-2.2)
def gen_source(source, n, fat, snf, lactose, protein, density, ph, water, freeze, cond):
    return pd.DataFrame({
        "Source": source,
        "Fat": np.round(np.random.normal(*fat, n), 2),
        "SNF": np.round(np.random.normal(*snf, n), 2),
        "Lactose": np.round(np.random.normal(*lactose, n), 2),
        "Protein": np.round(np.random.normal(*protein, n), 2),
        "Density": np.round(np.random.normal(*density, n), 1),
        "pH": np.round(np.random.normal(*ph, n), 2),
        "AddedWater": np.round(np.clip(np.random.exponential(water, n), 0, 40), 2),
        "FreezingPoint": np.round(np.random.normal(*freeze, n), 3),
        "Conductivity": np.round(np.random.normal(*cond, n), 2),
    })

n = 150
cow     = gen_source("Cow", n, (4.0,0.4), (8.7,0.3), (4.7,0.2), (3.3,0.2), (1029,2), (6.6,0.15), 5, (-0.53,0.02), (4.5,0.3))
buffalo = gen_source("Buffalo", n, (7.5,0.6), (9.5,0.3), (4.9,0.2), (4.3,0.3), (1031,2), (6.7,0.15), 4, (-0.55,0.02), (4.2,0.3))
goat    = gen_source("Goat", n, (3.8,0.4), (8.9,0.3), (4.5,0.2), (3.5,0.2), (1030,2), (6.5,0.15), 3, (-0.54,0.02), (4.7,0.3))
mixed   = gen_source("Mixed", n, (5.0,0.5), (9.0,0.3), (4.7,0.2), (3.7,0.2), (1030,2), (6.6,0.15), 4, (-0.54,0.02), (4.4,0.3))

df = pd.concat([cow, buffalo, goat, mixed], ignore_index=True)

locations = ["Bengaluru", "Mysuru", "Hassan", "Belagavi", "Hubballi-Dharwad",
             "Mangaluru", "Ballari", "Shivamogga", "Mandya", "Kalaburagi",
             "Tumakuru", "Davanagere"]
high_risk = {"Hassan", "Ballari", "Shivamogga", "Mandya", "Belagavi", "Hubballi-Dharwad"}

df["Location"] = np.random.choice(locations, size=len(df))
risk_multiplier = df["Location"].apply(lambda x: 1.8 if x in high_risk else 1.0)
df["AddedWater"] = np.round(df["AddedWater"] * risk_multiplier, 2).clip(0, 40)

antibiotic_prob = np.where(df["Location"].isin(high_risk), 0.12, 0.05)
df["AntibioticPresence"] = np.random.binomial(1, antibiotic_prob)

def classify(row):
    if row["AddedWater"] > 15 or row["AntibioticPresence"] == 1:
        return "Low Quality"
    elif row["pH"] < 6.4:
        return "Fermented"
    return "Standard"

df["Classification"] = df.apply(classify, axis=1)
df = df[["Location", "Source", "Fat", "SNF", "Lactose", "Protein", "Density", "pH",
         "AddedWater", "AntibioticPresence", "FreezingPoint", "Conductivity", "Classification"]]

# STEP 2: PREPROCESSING (Report Sec 2.3)
df["Source"] = df["Source"].astype("category")
df["Location"] = df["Location"].astype("category")
df["Classification"] = df["Classification"].astype("category")
numeric_cols = ["Fat", "SNF", "Lactose", "Protein", "Density", "pH",
                "AddedWater", "FreezingPoint", "Conductivity"]
df[numeric_cols] = df[numeric_cols].astype(float)
df.to_csv("milk_quality_dataset_karnataka.csv", index=False)

# STEP 3: CORRELATION ANALYSIS (Report Sec 3.2)
corr = df[numeric_cols].corr(method="pearson")
plt.figure(figsize=(9, 7))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, square=True, linewidths=0.5)
plt.title("Pearson Correlation Matrix of Physicochemical Milk Quality Variables")
plt.tight_layout()
plt.savefig("correlation_matrix.png", dpi=150)
plt.close()

# STEP 4: COMPARISON ACROSS MILK SOURCES (Report Sec 3.3)
group_means = df.groupby("Source", observed=True)[["Fat", "SNF", "Protein", "pH"]].mean()
group_means.plot(kind="bar", figsize=(9, 6))
plt.title("Comparison of Physicochemical Milk Quality Indicators by Source")
plt.ylabel("Mean Value")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("source_comparison.png", dpi=150)
plt.close()

# STEP 5: LOCATION-WISE ADULTERATION SUMMARY
location_summary = df.groupby("Location", observed=True).agg(
    AvgAddedWater=("AddedWater", "mean"),
    AntibioticRate=("AntibioticPresence", "mean"),
    LowQualityCount=("Classification", lambda x: (x == "Low Quality").sum())
).sort_values("LowQualityCount", ascending=False)

location_summary["LowQualityCount"].plot(kind="bar", figsize=(9, 6), color="firebrick")
plt.title("Low Quality Milk Samples by Karnataka Location")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("location_lowquality.png", dpi=150)
plt.close()

# STEP 6: HYPOTHESIS TESTING (Report Sec 2.4 gap addressed)
def pearson_ci(x, y, alpha=0.05):
    r, p = pearsonr(x, y)
    nn = len(x)
    z = np.arctanh(r)
    se = 1 / np.sqrt(nn - 3)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    lo, hi = np.tanh(z - z_crit * se), np.tanh(z + z_crit * se)
    return r, p, lo, hi

corr_pairs = [("Fat", "SNF"), ("pH", "SNF"), ("AddedWater", "Density"), ("AddedWater", "FreezingPoint")]
corr_results = []
for a, b in corr_pairs:
    r, p, lo, hi = pearson_ci(df[a], df[b])
    sig = "significant" if p < 0.05 else "not significant"
    corr_results.append([a, b, r, p, lo, hi, sig])
pd.DataFrame(corr_results, columns=["Var1","Var2","r","p_value","CI_low","CI_high","Significance"]).to_csv("correlation_significance.csv", index=False)

anova_results = []
for col in ["Fat", "SNF", "Protein", "pH"]:
    groups = [df[df["Source"] == s][col].values for s in df["Source"].unique()]
    f_stat, p_val = f_oneway(*groups)
    sig = "significant" if p_val < 0.05 else "not significant"
    anova_results.append([col, f_stat, p_val, sig])
pd.DataFrame(anova_results, columns=["Variable","F_statistic","p_value","Significance"]).to_csv("anova_results.csv", index=False)

buffalo_fat = df[df["Source"]=="Buffalo"]["Fat"]
cow_fat = df[df["Source"]=="Cow"]["Fat"]
t1, p1 = ttest_ind(buffalo_fat, cow_fat, equal_var=False)

goat_ph = df[df["Source"]=="Goat"]["pH"]
cow_ph = df[df["Source"]=="Cow"]["pH"]
t2, p2 = ttest_ind(goat_ph, cow_ph, equal_var=False)

pd.DataFrame([
    ["Buffalo vs Cow", "Fat", t1, p1],
    ["Goat vs Cow", "pH", t2, p2]
], columns=["Comparison","Variable","t_statistic","p_value"]).to_csv("ttest_results.csv", index=False)

contingency = pd.crosstab(df["Location"], df["Classification"])
chi2, p_chi, dof, expected = stats.chi2_contingency(contingency)

# STEP 7: CLASSIFICATION WITH SMOTE (Report Sec 3.4)
le = LabelEncoder()
X = df[numeric_cols + ["AntibioticPresence"]]
y = le.fit_transform(df["Classification"])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

sm = SMOTE(random_state=42)
X_train_bal, y_train_bal = sm.fit_resample(X_train, y_train)

clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X_train_bal, y_train_bal)
preds = clf.predict(X_test)
print(classification_report(y_test, preds, target_names=le.classes_))

importances = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False)
importances.plot(kind="barh", figsize=(8, 6))
plt.title("Random Forest Feature Importance")
plt.xlabel("Importance")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=150)
plt.close()

# STEP 8: CROSS-VALIDATION (Future Work, Report Sec 3.6)
cv_scores = cross_val_score(clf, X_train_bal, y_train_bal, cv=5)
print("5-Fold CV Accuracy:", round(cv_scores.mean(),3), "+/-", round(cv_scores.std(),3))
