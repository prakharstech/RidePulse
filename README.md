# 🚖 RidePulse: Self-Healing MLOps Platform

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![AWS](https://img.shields.io/badge/Cloud-AWS_Lambda-orange?logo=amazon-aws)
![Docker](https://img.shields.io/badge/Container-Docker-blue?logo=docker)
![CI/CD](https://img.shields.io/badge/Pipeline-GitHub_Actions-green?logo=github-actions)
![FastAPI](https://img.shields.io/badge/API-FastAPI-teal?logo=fastapi)

**RidePulse** is an End-to-End MLOps system designed to predict taxi fares in real-time. Unlike static models, RidePulse features a **"Self-Healing" pipeline** that detects data drift (simulated via API) and automatically triggers a cloud-based retraining and deployment workflow without human intervention.

---

## 🏗️ Architecture

The system follows a modern Serverless MLOps architecture:

```mermaid
graph LR
  A[Client Request] -->|REST API| B(AWS Lambda)
  B -->|Inference| C{Model Version}
  C -->|Normal| D[Standard Fare]
  C -->|Drift Detected| E[Trigger GitHub Action]
  E -->|Retrain & Deploy| F[GitHub Actions Runner]
  F -->|Push Image| G[AWS ECR]
  G -->|Update Code| B

  ## 🚀 Key Features

* **Serverless Inference:** Deployed on **AWS Lambda** via Container Images (ECR) for auto-scaling and zero-idle costs.
* **Self-Healing Pipeline:** A fully automated CI/CD workflow that retrains the XGBoost model when "Market Drift" is detected.
* **Chaos Engineering Mode:** An innovative `/simulate-drift` endpoint that artificially inflates market prices to test the system's ability to adapt.
* **Containerized Environment:** Dockerized application ensures consistency across development, testing, and production.
* **FastAPI Backend:** High-performance, asynchronous API for handling prediction requests.

---

## 🛠️ Tech Stack

* **Language:** Python 3.12
* **Machine Learning:** XGBoost, Scikit-Learn, Pandas
* **API Framework:** FastAPI, Uvicorn
* **Containerization:** Docker
* **Cloud Provider:** AWS (Lambda, ECR)
* **CI/CD:** GitHub Actions (Custom "Retrain & Deploy" Workflow)

---

## 🕹️ Live Demo (The "Magic" Loop)

This project includes a built-in demo loop to showcase the MLOps lifecycle during interviews.

### 1. Check Baseline (Normal Mode)
Send a prediction request for a standard 5-mile trip.

* **Endpoint:** `POST /predict`
* **Payload:**
    ```json
    { "trip_distance": 5, "PULocationID": 132, "DOLocationID": 230, "hour": 17, "day_of_week": 1 }
    ```
* **Expected Output:** `~ $26.19` (Standard Fare)

### 2. Simulate Market Drift (Chaos Mode)
Trigger the simulation to mimic a surge in prices (e.g., heavy rain or holidays).

* **Endpoint:** `POST /simulate-drift`
* **Action:** This sends a signal to GitHub Actions to launch the **Retraining Pipeline**.
* **Status:** *Wait ~3-5 minutes for the cloud pipeline to retrain and update AWS Lambda.*

### 3. Verify Self-Healing
Send the *same* prediction request as Step 1.

* **Endpoint:** `POST /predict`
* **Expected Output:** `~ $38.28` (Inflated Fare)
* **Result:** The system successfully detected the drift, retrained, and deployed the new model automatically.

### 4. Reset
Restore the system to its original state.

* **Endpoint:** `POST /reset-model`

---

## 📦 Installation & Local Setup

To run the inference API locally:

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/prakharstech/RidePulse.git](https://github.com/prakharstech/RidePulse.git)
    cd RidePulse
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the API**
    ```bash
    uvicorn app.main:app --reload
    ```
    *Access Swagger UI at: `http://127.0.0.1:8000/docs`*

---

## 🐳 Docker Deployment

To build and run the container locally:

```bash
# Build the image (stripping metadata for AWS compatibility)
docker build --platform linux/amd64 --provenance=false -t ridepulse-repo .

# Run the container
docker run -p 8080:8080 ridepulse-repo

## ☁️ Cloud Deployment (AWS)

Deployment is handled automatically via GitHub Actions.

* **Push to Main:** Any push to the `main` branch triggers the pipeline (optional configuration).
* **Manual Trigger:** The pipeline listens for `repository_dispatch` events triggered by the `/simulate-drift` or `/reset-model` endpoints.
* **Secrets:** The repository requires `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION` to be configured in GitHub Secrets.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

**Author:** [Prakhar Srivastava](https://github.com/prakharstech)