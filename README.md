# decodelabs_data_cleaning_project
Data cleaning and preparation project using Excel Power Query and Python (pandas)
# Data Cleaning & Preparation Project

Project 1 of the DecodeLabs Data Analytics internship track.

## Goal
Clean a raw e-commerce orders dataset (1,200 rows, 14 columns) by handling
missing values, duplicates and incorrect formats.

## Tools
- Excel Power Query
- Python (pandas)

## What I did
- Filled 309 blank CouponCode values with "No Coupon" (a blank meant no coupon was used)
- Checked for duplicate OrderIDs (0 found)
- Trimmed text, checked for case inconsistencies, rounded prices to 2 decimals
- Set dates to YYYY-MM-DD (ISO 8601)
- Verified: 0 duplicate IDs, 0 invalid dates, 0 empty cells

## Files
- `project1_cleaning.py`: the Python cleaning script
- `Dataset_Cleaned_Python.xlsx`: cleaned dataset
- `Project1_Change_Log.pdf`: change log with proof of verification
