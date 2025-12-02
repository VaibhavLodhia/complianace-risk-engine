# Predictive Data Governance and Compliance Risk Engine

A two-stage predictive compliance risk engine that combines unsupervised anomaly detection with supervised classification to identify policy violations in data access logs. This system is designed for HIPAA/GDPR-regulated environments to automatically detect and score compliance risks.

## 🎯 Overview

This project implements a hybrid machine learning approach to compliance monitoring:

1. **Stage 1 - Unsupervised Anomaly Detection**: Uses Isolation Forest to detect unusual access patterns without labeled data
2. **Stage 2 - Supervised Classification**: Uses XGBoost to predict policy violations based on anomaly scores and metadata

The system generates a **Compliance Infraction Score** (0-1 probability) for each access event, enabling security teams to prioritize investigations.

## 🏗️ Architecture

```
Raw Access Logs → Isolation Forest → Anomaly Scores → XGBoost → Compliance Infraction Scores
     ↓                    ↓                ↓              ↓                    ↓
  Metadata          Unsupervised      Feature        Supervised         Risk Ranking
                   Detection         Integration    Classification
```

## ✨ Features

### Data Generation
- **Synthetic Data Creation**: Generates realistic metadata and access logs
- **Anomaly Injection**: Deliberately injects 2,500 high-risk anomalies for training
- **Policy Violation Labeling**: Automatically labels violations based on three criteria:
  - Access to Plain text PHI assets
  - Access outside business hours (9 PM - 5 AM)
  - Access from non-US IP addresses

### Machine Learning Pipeline
- **Isolation Forest**: Unsupervised anomaly detection with configurable contamination rate
- **XGBoost Classifier**: Gradient boosting model for binary classification
- **Feature Engineering**: Time-based features (hour, day, month) and one-hot encoding
- **Model Evaluation**: Comprehensive classification report with precision, recall, and F1-scores

### Risk Scoring
- **Anomaly Score**: Continuous value indicating how anomalous an access pattern is
- **Compliance Infraction Score**: Probability (0-1) of a policy violation
- **Top Risk Identification**: Automatically identifies highest-risk access events

## 📋 Requirements

- Python 3.8+
- pandas >= 1.5.0
- numpy >= 1.23.0
- scikit-learn >= 1.2.0
- xgboost >= 1.7.0

## 🚀 Installation

1. Clone the repository or navigate to the project directory:
```bash
cd project1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Step 1: Generate Data

First, generate the synthetic data and save it to CSV files:

```bash
python generate_data.py
```

This will create:
- `data/metadata.csv` - 500 data assets with PHI flags and encryption status
- `data/access_logs.csv` - 100,000 access log entries with policy violation labels

### Step 2: Run Compliance Risk Engine

Run the main analysis script:

```bash
python compliance_risk_engine.py
```

The script will:
1. Load data from CSV files
2. Train Isolation Forest model for anomaly detection
3. Train XGBoost classifier for compliance violation prediction
4. Generate risk scores for all access events
5. Display classification report and top 5 highest-risk records

## 📊 Output

### Classification Report
Detailed performance metrics including:
- Precision, Recall, F1-score for Normal vs. Violation classes
- Support (number of samples)
- Overall accuracy

### Top 5 Highest-Risk Records
For each high-risk access event, displays:
- Timestamp
- User ID
- Data Asset ID
- Access Type (Read/Write)
- IP Location
- Anomaly Score
- Compliance Infraction Score
- Actual and Predicted Violation Status



## 🔧 Technical Details

### Data Specifications
- **Metadata**: 500 data assets
- **Access Logs**: 100,000 entries
- **Users**: 100 unique users
- **Time Range**: 6 months of data
- **Anomalies**: 2,500 injected high-risk events

### Model Configuration
- **Isolation Forest**:
  - n_estimators: 100
  - contamination: 0.025 (2.5%)
  - random_state: 42

- **XGBoost**:
  - n_estimators: 100
  - max_depth: 6
  - learning_rate: 0.1
  - random_state: 42

### Feature Set
- Time features: Hour_of_Day, Day_of_Week, Day_of_Month, Month
- Categorical (one-hot encoded): Access_Type, IP_Location, Encryption_Status
- Metadata: PHI_Flag
- Derived: Anomaly_Score from Stage 1

## 🎯 Use Cases

- **Security Operations**: Identify suspicious access patterns in real-time
- **Compliance Monitoring**: Automatically detect HIPAA/GDPR policy violations
- **Risk Prioritization**: Focus investigation efforts on highest-risk events
- **Audit Support**: Generate evidence and reports for compliance audits
- **Anomaly Detection**: Discover unknown threats through unsupervised learning

## 🔄 Workflow

1. **Data Generation** (`generate_data.py`):
   - Creates synthetic metadata and access logs
   - Injects anomalies based on violation criteria
   - Saves data to CSV files for reproducibility

2. **Anomaly Detection** (`compliance_risk_engine.py` - Part 2):
   - Extracts time-based and categorical features
   - Trains Isolation Forest model
   - Generates anomaly scores for all records

3. **Compliance Classification** (`compliance_risk_engine.py` - Part 3):
   - Integrates anomaly scores with metadata features
   - Trains XGBoost classifier
   - Predicts violation probabilities
   - Ranks access events by risk

## 📈 Model Performance

The two-stage approach achieves high accuracy by:
- **Stage 1** catching unknown anomalies through pattern detection
- **Stage 2** leveraging domain knowledge (PHI flags, encryption status) for precise classification

## 🔐 Reproducibility

All random operations use `random_state=42` to ensure:
- Consistent data generation across runs
- Reproducible model training
- Same results when re-running the pipeline

## 📝 Notes

- Data files are excluded from version control (see `.gitignore`)
- Run `generate_data.py` first before running the main script
- The system is designed for demonstration purposes with synthetic data
- In production, replace data generation with real access log ingestion

## 🤝 Contributing

This is a demonstration project. For production use, consider:
- Real-time data ingestion pipelines
- Model retraining schedules
- Alerting and notification systems
- User authentication and authorization
- Audit logging and compliance reporting

## 📄 License

This project is for educational and demonstration purposes.
