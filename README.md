# Project Haalu — A Study of Milk Types and Their Correlation with Quality Variables

**Service Learning Report | Department of Mathematics, CHRIST (Deemed to be University), Bengaluru | March 2025**

[![Python](https://img.shields.io/badge/Python-3.12-blue)]() [![scikit-learn](https://img.shields.io/badge/scikit--learn-RandomForest-orange)]() [![License](https://img.shields.io/badge/License-Academic-lightgrey)]()

## Overview

Project Haalu is a statistical analysis of physicochemical milk-quality variables across four milk sources — cow, buffalo, goat, and mixed milk. Beyond descriptive correlation analysis, this extended version adds formal hypothesis testing, a Random Forest classification pipeline with class balancing, and a supplementary geographic dimension across Karnataka districts to study adulteration risk patterns.

## Objectives

- Construct a representative, literature-grounded dataset of physicochemical milk-quality variables across cow, buffalo, goat, and mixed milk, with transparent documentation of provenance
- Analyze correlations between milk quality indicators (fat, SNF, protein, pH, added water) and validate them with formal significance testing
- Compare nutritional and physicochemical properties across the four milk sources using ANOVA and pairwise t-tests
- Explore whether a Random Forest classifier can distinguish Standard/Low Quality/Fermented labels from physicochemical variables
- Test whether randomized Karnataka sampling location shows a statistical association with adulteration classification
- Offer data-informed, appropriately hedged suggestions for milk storage, adulteration detection, and processing practice

## Dataset

The dataset was **synthetically constructed** using representative physicochemical value ranges drawn from published dairy-science literature and open milk-quality datasets — it is not a set of laboratory-measured samples. It reflects typical relationships reported in the literature, not measured samples of milk actually sold in Karnataka.

| Variable | Unit | Description |
|---|---|---|
| Location | — | Randomized Karnataka sampling district (12 categories) |
| Source | — | Milk source category: Cow, Buffalo, Goat, or Mixed |
| Fat | % | Fat content as a percentage of total milk volume |
| SNF | % | Solids-not-fat: total solids excluding fat |
| Lactose | % | Lactose (milk sugar) content |
| Protein | % | Total protein content |
| Density | kg/m³ | Mass per unit volume of the milk sample |
| pH | — | Acidity/alkalinity on the standard pH scale |
| Added Water | % | Estimated proportion of added (diluting) water |
| Antibiotic Presence | Binary | Whether antibiotic residue is flagged as present |
| Freezing Point | °C | Freezing point, used as an adulteration indicator |
| Conductivity | mS/cm | Electrical conductivity of the milk sample |
| Classification | Categorical | Standard, Low Quality, or Fermented |

**Sample size:** 600 records (150 per source)

## Methodology

1. Literature review of typical physicochemical ranges reported for cow, buffalo, goat, and mixed milk
2. Definition of representative sampling ranges for each variable, by source
3. Generation of a synthetic base dataset by sampling within these ranges
4. Randomized assignment of Karnataka sampling location, with added-water and antibiotic rates weighted upward for districts flagged in state surveillance drives as higher-risk
5. Exploratory data analysis, Pearson correlation analysis, and visualization
6. Formal statistical significance testing (correlation p-values/CIs, ANOVA, t-tests, chi-square)
7. Supplementary classification exercise using Random Forest with SMOTE class balancing and 5-fold cross-validation

## Key Findings

### Correlation Analysis

| Relationship | r | p-value | 95% CI | Significance |
|---|---|---|---|---|
| Fat ↔ SNF | 0.612 | 5.02e-63 | [0.560, 0.660] | Significant |
| pH ↔ SNF | 0.206 | 3.73e-07 | [0.128, 0.281] | Significant |
| Added Water ↔ Density | -0.068 | 0.095 | [-0.147, 0.012] | Not significant |
| Added Water ↔ Freezing Point | 0.017 | 0.674 | [-0.063, 0.097] | Not significant |

### Source Comparison (ANOVA + t-tests)

- **Buffalo milk** showed the highest fat (~7.55%) and protein (~4.28%) content, consistent with literature reporting buffalo milk fat content roughly double that of cow milk
- **Cow milk** showed comparatively stable pH (~6.63) and moderate fat content (~3.97%)
- **Goat milk** showed lower fat (~3.84%) but the lowest mean pH (~6.50) among all sources
- **Mixed milk** fell between single-source categories (~4.99% fat), consistent with being modelled as a blend
- All four variables (Fat, SNF, Protein, pH) differ significantly across sources (ANOVA, p < 0.001 for each)
- Buffalo vs Cow (Fat): t = 61.76, p < 0.001 — significant
- Goat vs Cow (pH): t = -7.24, p < 0.001 — significant

### Classification Performance

| Class | Precision | Recall | F1-score |
|---|---|---|---|
| Fermented | 1.00 | 1.00 | 1.00 |
| Low Quality | 0.86 | 1.00 | 0.93 |
| Standard | 1.00 | 0.97 | 0.98 |

**Overall test accuracy:** 97% · **5-fold CV accuracy:** 99.7% ± 0.2%

Top predictive features: pH (0.41), Added Water (0.23), Antibiotic Presence (0.23). Note: since the Classification label itself was rule-derived from these variables, this accuracy reflects the labeling logic rather than a validated real-world detection capability — see Limitations below.

### Location-Wise Adulteration Pattern (Supplementary)

A chi-square test found a statistically significant association between sampling location and quality classification (χ² = 50.77, dof = 22, p = 0.00046). Belagavi, Mandya, and Hassan showed the highest counts of Low Quality samples in this simulation, loosely reflecting real-world FSSAI surveillance reports — though locations were randomly assigned and risk-weighted manually, so this should be read as a methodological demonstration, not a factual claim about real milk quality in these districts.

## Tech Stack

Python · Pandas · NumPy · SciPy (hypothesis testing) · scikit-learn (Random Forest) · imbalanced-learn (SMOTE) · Matplotlib · Seaborn

## Repository Structure
Project-Haalu/
├── data/
│ └── milk_quality_dataset_karnataka.csv
├── notebooks/
│ └── project_haalu_end_to_end.py
├── results/
│ ├── correlation_significance.csv
│ ├── anova_results.csv
│ └── ttest_results.csv
├── figures/
│ ├── correlation_matrix.png
│ ├── source_comparison.png
│ ├── location_lowquality.png
│ └── feature_importance.png
├── report/
│ └── Project_Haalu_Report.pdf
└── README.md

text

## Running the Pipeline

```bash
pip install pandas numpy scipy scikit-learn imbalanced-learn matplotlib seaborn
python notebooks/project_haalu_end_to_end.py
```

## Limitations

- Dataset is synthetically constructed from literature-reported ranges, not laboratory-measured samples
- Two of four tested correlations (Added Water ↔ Density, Added Water ↔ Freezing Point) were **not** statistically significant, qualifying the expected dilution-effect narrative
- Classification accuracy is inflated by label circularity — the Classification field was derived from a subset of the model's own input features
- Location-based adulteration patterns use randomly assigned locations with manually specified risk weights, not real geotagged samples
- No time-series or microbiological data, so spoilage-related discussion is drawn from literature rather than the dataset itself
- Correlations should not be interpreted as evidence of causation

## Future Directions

- Validate patterns against real, laboratory-measured milk samples from Karnataka dairies
- Refit location-risk weighting against real district-level surveillance data
- Re-run classification with an independently defined quality label to avoid circularity
- Incorporate time-series or microbiological measurement of spoilage
- Benchmark adulteration detection (pH, added water, freezing point) against FSSAI thresholds

## Acknowledgements

This project was completed under the guidance of Dr. Smita S. Nagouda and Dr. Tabitha Rajashekar, Department of Mathematics, CHRIST (Deemed to be University).

## Author

**Kavin Narayanan**
BSc Mathematics, Economics and Statistics, CHRIST (Deemed to be University), Bengaluru
BS Data Science and Applications, IIT Madras

## License

Submitted as part of academic coursework; shared here for portfolio purposes.
