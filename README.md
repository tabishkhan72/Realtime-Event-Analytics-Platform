# Realtime Event Analytics Platform


A **scalable microservices-based system** for ingesting, processing, and visualizing realtime events. This project highlights distributed systems design, data streaming, caching, and cloud-native deployment practices — making it a strong showcase for SDE roles.


---


## 🚀 Features
- **Event Ingestion**: FastAPI microservice that receives JSON events and publishes them to Kafka.
- **Stream Processing**: Kafka consumer that updates Redis for realtime stats and persists events to PostgreSQL.
- **Analytics API**: FastAPI service exposing REST endpoints for realtime and historical analytics.
- **Realtime Dashboard**: React-based UI to visualize metrics and trends with live updates.
- **Caching**: Redis for low-latency reads.
- **Persistence**: PostgreSQL for durable event storage.
- **Deployment**: Docker Compose for local dev, Kubernetes manifests for scalable cloud deployment.
- **CI/CD Ready**: Can be extended with GitHub Actions for automated testing and deployment.


---


## 🏗 Architecture Overview
```
+-----------------+
| Ingestion API | ---> Kafka ---> [ Processor Service ]
+-----------------+ | |
v v
Redis PostgreSQL
| |
Realtime Historical
| |
+---------------------+
| Analytics API |
+---------------------+
|
React Dashboard
```


---


## 📂 Project Structure
```
realtime-analytics-platform/
├── backend/
│ ├── ingestion_service/ # FastAPI ingestion microservice
│ ├── processor_service/ # Kafka consumer & Redis/Postgres writer
│ ├── analytics_api/ # FastAPI analytics endpoints
├── frontend/ # React dashboard
├── k8s/ # Kubernetes manifests
├── docker-compose.yml # Local dev orchestration
└── README.md # Project docs
```


---


## ⚙️ Tech Stack
- **Backend**: Python (FastAPI), Kafka, Redis, PostgreSQL
- **Frontend**: React, Recharts/D3.js
- **Infra**: Docker, Kubernetes
- **Orchestration**: Airflow (optional for batch jobs)
- **CI/CD**: GitHub Actions (extendable)


---


## 🖥️ Usage
### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/realtime-analytics-platform.git
cd realtime-analytics-platform
```


### 2. Start services
```bash
docker-compose up --build
```


### 3. Access the platform
- Ingestion API: [http://localhost:8000/docs](http://localhost:8000/docs)
- Analytics API: [http://localhost:8002/docs](http://localhost:8002/docs)
- Dashboard: [http://localhost:3000](http://localhost:3000)


---


---
