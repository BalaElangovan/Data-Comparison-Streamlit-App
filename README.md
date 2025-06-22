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

## How to Run

```bash
pip install -r requirements.txt
streamlit run compare_app.py
```

## Why Streamlit?

This project uses Streamlit as the primary framework to build an interactive and user-friendly web interface for comparing Excel or CSV files. Streamlit simplifies the development of data-driven web applications using pure Python—no HTML, CSS, or JavaScript required.


📁 File Upload Widgets:	Let users upload two Excel or CSV files directly through the browser.

🎛️ Interactive Controls:	Enables column selection, key field identification, and resampling with the click of a button.

📊 Data Visualisation: 	Displays Excel/CSV content and comparison results using st.dataframe and styled tables.

🎯 Change Detection:	Highlights modified cell values in real-time, improving visibility for QA and data review tasks.

☁️ Easy Deployment: Allows effortless deployment to Streamlit Cloud, enabling others to use the app without installation.


By using Streamlit, we were able to rapidly prototype and deploy a comparison tool that is both powerful and accessible, even to non-technical users.
