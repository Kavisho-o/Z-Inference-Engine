# ZEPHYR-ML  
### Explainable Journey Risk Intelligence Engine

**ZEPHYR-ML** is an analytical machine learning framework designed to **predict and interpret travel risk at the route-segment level**.

Unlike traditional black-box risk systems, ZEPHYR-ML breaks predictions into **human-readable explanations**, showing *exactly why* a route segment is risky.

The system uses:

- Synthetic data modeled on Indian road conditions  
- Rule-based supervision for deterministic labeling  
- SHAP (SHapley Additive exPlanations) for transparent ML predictions  

---

## Problem Statement

Travel risk is influenced by many interacting variables:

- Weather  
- Terrain  
- Traffic density  
- Time and visibility conditions  

Most existing systems output **binary decisions or opaque scores**, offering **no insight into why** a route is considered dangerous.

### ZEPHYR-ML solves this by:

- Modeling risk as a **continuous score (0–100)**  
- Breaking journeys into **individual route segments**  
- Generating **per-prediction explanations** for transparency and auditability  

---

## System Capabilities

### 🔹 Segment-Level Analysis  
Decomposes long journeys into **granular route segments** for precise risk evaluation.

### 🔹 Continuous Risk Quantification  
Predicts a numerical risk score and maps it into interpretable tiers:

| Score Range | Category   |
|------------|-----------|
| 0–30       | Safe      |
| 31–60      | Moderate  |
| 61–100     | Dangerous |

### 🔹 Explainable AI (XAI)  
Uses SHAP to measure how much each feature contributed to the final risk score.

### 🔹 Production-Oriented Design  
Built as a **modular backend ML engine**, not a research notebook.

---

## Technical Differentiators

ZEPHYR-ML prioritizes **interpretability, reliability, and robustness**.

### 🧠 Custom Synthetic Data  
No dependency on external datasets. A custom engine simulates realistic Indian road environments.

### 📏 Deterministic Labeling  
A rule-based "teacher" model generates training labels aligned with domain logic.

### 🌧 Stress Testing  
Validated under **distribution shifts**, including:

- Monsoon vs. non-monsoon conditions  
- Extreme terrain variations  

### 📈 Regression-First Modeling  
Risk is modeled as a **continuous variable**, avoiding shortcuts of classification-only approaches.

---

## High-Level Architecture

ZEPHYR-ML follows a modular ML pipeline:

1. **Generation**  
   Synthetic route and environmental context creation  

2. **Engineering**  
   Deterministic feature transformation and encoding  

3. **Labeling**  
   Domain-specific risk rules generate training targets  

4. **Modeling**  
   Random Forest regression captures complex non-linear relationships  

5. **Explainability**  
   SHAP integration decomposes each prediction into feature contributions  

---

## Example Inference Output

**Predicted Risk Score:** `37.43` → **Moderate Risk**

### 🚨 Primary Risk Drivers
- **Time of Day** — Night driving increased the risk coefficient  
- **Visibility** — Fog/rain reduced clarity and raised risk  

### 🟢 Mitigating Factors
- **Precipitation** — Low rainfall intensity reduced hazard level  
- **Terrain** — Favorable road geometry offset environmental risks  

---

## Installation & Execution

Run the standalone demonstration locally:

```bash
git clone <repository-url>
cd zephyr-ml
pip install -r requirements.txt
python standalone/run_demo.py
```

---

## Project Roadmap

### 🚀 Inference API  
FastAPI or Django wrapper for real-time predictions

### 🧮 Journey-Level Aggregation  
Combine segment scores into a complete journey risk profile

### 🌍 Real-World Integration  
Pipeline extensions for:

- Live telemetry ingestion  
- Weather API integration  

---

## Current Status

| Component | Status |
|----------|--------|
| Data Generation & ML Pipeline | ✅ Functional & Validated |
| Explainability Layer | ✅ Fully Integrated |
| Backend API Integration | 🚧 In Development |
