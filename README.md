# Project Haalu — A Study of Milk Types and Their Correlation with Quality Variables

Service Learning Report | Department of Mathematics, CHRIST (Deemed to be University), Bengaluru | March 2025

## Overview

Project Haalu is a descriptive and correlational analysis of physicochemical milk-quality variables across four milk sources — cow, buffalo, goat, and mixed milk . The study examines relationships between key quality indicators such as fat, solids-not-fat (SNF), protein, pH, and added-water percentage to assess milk purity, nutritional adequacy, and possible adulteration .

## Objectives

- Construct a representative, literature-grounded dataset of physicochemical milk-quality variables across cow, buffalo, goat, and mixed milk, with transparent documentation of its provenance 
- Analyze correlations between milk quality indicators (fat, SNF, protein, pH, added water) 
- Compare nutritional and physicochemical properties across the four milk sources 
- Review literature on how microbial activity, storage temperature, and processing techniques affect milk spoilage and shelf life 
- Explore, as a supplementary exercise, whether a Random Forest classifier can distinguish Standard/Low Quality/Fermented labels from physicochemical variables 
- Offer data-informed, appropriately hedged suggestions for milk storage, adulteration detection, and processing practice 

## Dataset

The dataset was **synthetically constructed** using representative physicochemical value ranges drawn from published dairy science literature and open milk quality datasets, it is not a set of laboratory-measured samples. It is intended to reflect typical physicochemical relationships reported in the literature, not a measured sample of milk actually sold in Karnataka.

| Variable | Unit | Description |
|---|---|---|
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

## Methodology

1. Literature review of typical physicochemical ranges (fat, SNF, protein, pH, lactose, density, freezing point, conductivity) reported for cow, buffalo, goat, and mixed milk 
2. Definition of representative ranges for each variable, by source 
3. Generation of a synthetic base dataset by sampling within these ranges for each source category 
4. Exploratory data analysis, Pearson correlation analysis, and visualization 
5. Supplementary classification exercise using Random Forest to distinguish quality categories 

## Key Findings

- **Fat and SNF**: moderate positive correlation (r = 0.53), consistent with fat and non-fat solids moving together across milk sources 
- **pH and SNF**: moderate correlation (r = 0.65) — lower pH tended to co-occur with lower SNF 
- **Added Water and Density/Nutrient content**: negative correlation, consistent with the expected dilution effect 
- **Buffalo milk** showed the highest fat and protein content among the four sources, consistent with literature reporting buffalo milk fat content roughly double that of cow milk 
- **Cow milk** showed comparatively stable pH and moderate fat content 
- **Goat milk** showed lower fat but higher protein and lactose than cow milk, with a slightly lower pH 
- **Mixed milk** fell between single-source categories, consistent with being modelled as a blend 

> Note: correlations are descriptive; no formal significance testing (p-values, confidence intervals) was performed in this iteration.

## Tech Stack

Python, Pandas, Statistical Analysis (Pearson Correlation), Random Forest (scikit-learn), Data Visualization (heatmaps, comparison plots)


