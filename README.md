# Credit Card Fraud Classifier

This repository contains a production-friendly training pipeline to build a classifier for fraudulent credit card transactions.

## Overview

The training pipeline performs the following steps:
1. Load data from CSV using Pandas.
2. Data preprocessing:
    - Drop duplicates
    - Handle null values of numerical variables
    - Replace null categorical values with "MISSING_VALUE" string
3. Feature Selection
4. Model training with cross-validated search:
    - LightGBM
    - Random Forest
5. Performance metrics computation

