# Data Comparison Tool (Streamlit App)

This Streamlit web application enables users to upload and compare two Excel or CSV files—such as datasets from different time points or environments—to identify structural and content differences. 

It automatically detects added, removed, or modified columns, highlights changes in cell values across shared rows, and supports intelligent sampling by identifying key columns (e.g., NHSNumber, ClientID, RioID). 

The app displays a side-by-side or stacked visual comparison of matched rows, with differences highlighted in colour. It also includes a "Resample" button to randomly compare different records without manual input, making the review process quick, user-friendly, and efficient for QA analysts, healthcare staff, data engineers, and auditors working with dynamic datasets.

## Features
- Upload `.xlsx` or `.csv` files
- Auto-detect key columns (e.g., NHSNumber, ClientID, RioID)
- Randomly samples 4 records for data comparison
- Highlights text differences between old and new files
- Export result as Excel (optional)
- Resample button for new comparisons

## How to Run

```bash
pip install -r requirements.txt
streamlit run compare_app.py
