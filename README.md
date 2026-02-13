# ChainGuard AI

ChainGuard AI is an explainable fraud detection system designed for blockchain transaction analysis.

## Problem

Blockchain fraud detection systems often lack explainability. Analysts receive alerts without clear reasoning behind risk decisions.

## Solution

ChainGuard AI applies deterministic rule-based scoring to generate transparent risk scores (0–100) and clearly shows which rules triggered each alert.

## Features

- Explainable risk scoring engine
- Risk classification (Low / Medium / High)
- Dashboard with risk overview
- Rule impact analysis
- Investigation-friendly filtering

## Technology Stack

- Python
- Pandas
- Streamlit
- Matplotlib

## How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Run the application:
   streamlit run app.py

3. Upload a transaction CSV file to begin analysis.

## Future Enhancements

- Live blockchain API integration
- Custom analyst-defined rules
- Automated compliance reporting
