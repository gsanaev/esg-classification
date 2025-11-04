# Classifying Corporate ESG Performance Using Machine Learning

**Golib Sanaev — November 2025**

---

## Overview

`esg-classification` explores the relationship between **Environmental, Social, and Governance (ESG)** indicators and firm-level financial performance using modern machine learning techniques.

The project is based on the **ESG and Financial Performance Dataset** from *Kaggle*, which provides simulated firm-level ESG metrics and financial outcomes suitable for modeling and benchmarking.  
It applies algorithms such as **logistic regression**, **random forests**, and **gradient boosting** to classify firms according to sustainability-driven performance patterns.

---

## Background

Earlier stages of this work focused on integrating real-world ESG indicators from **OECD** and **EU Taxonomy** sources.  
Insights from that data engineering phase helped define the structure and modeling approach used in this project.  
The current version focuses on machine learning experimentation and model interpretability using structured, publicly available data.

---

## Objectives

- Examine how ESG indicators relate to financial outcomes.  
- Benchmark several classification algorithms on ESG features.  
- Identify which ESG dimensions (E, S, or G) most strongly influence firm performance.  
- Provide interpretable visualizations and model evaluation metrics (ROC-AUC, F1-score, feature importance).

---

## Methodology

1. **Data Acquisition**  
   - Download the *ESG and Financial Performance Dataset* from Kaggle.  
   - Clean and preprocess the data for consistency and modeling.

2. **Feature Engineering**  
   - Handle missing values, normalize numerical variables, and encode categorical ones.  
   - Derive composite ESG indices where appropriate.

3. **Modeling**  
   - Train baseline and advanced classification models:
     - Logistic Regression  
     - Random Forest Classifier  
     - Gradient Boosting (XGBoost / LightGBM)

4. **Evaluation**  
   - Assess models using cross-validation and metrics such as accuracy, ROC-AUC, and F1-score.  
   - Visualize feature importance to interpret model outputs.

---

## Planned Repository Structure

