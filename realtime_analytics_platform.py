# Realtime Event Analytics Platform
# Project scaffold for GitHub resume project

# Directory Structure:
# realtime-analytics-platform/
# ├── backend/
# │   ├── ingestion_service/
# │   │   ├── main.py
# │   │   ├── requirements.txt
# │   ├── processor_service/
# │   │   ├── main.py
# │   │   ├── requirements.txt
# │   ├── analytics_api/
# │   │   ├── main.py
# │   │   ├── requirements.txt
# ├── frontend/
# │   ├── package.json
# │   ├── src/
# │   │   ├── App.js
# │   │   ├── components/
# │   │   │   ├── Dashboard.js
# ├── docker-compose.yml
# ├── k8s/
# │   ├── deployment.yaml
# │   ├── service.yaml
# ├── README.md

###############################################
# backend/ingestion_service/main.py
###############################################
from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import json

app = FastAPI()
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class Event(BaseModel):
    userId: int
    action: str
    timestamp: str

@app.post("/ingest")
async def ingest_event(event: Event):
    producer.send("events", event.dict())
    return {"status": "event ingested"}

###############################################
# backend/processor_service/main.py
###############################################
from kafka import KafkaConsumer
import redis, json, psycopg2

consumer = KafkaConsumer(
    'events',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

r = redis.Redis(host='redis', port=6379, db=0)

conn = psycopg2.connect(dbname="events", user="postgres", password="postgres", host="postgres")
cur = conn.cursor()

for msg in consumer:
    event = msg.value
    # Update Redis (realtime)
    r.incr(f"user:{event['userId']}:actions")
    # Insert into PostgreSQL
    cur.execute("INSERT INTO events(userId, action, timestamp) VALUES (%s, %s, %s)",
                (event['userId'], event['action'], event['timestamp']))
    conn.commit()

###############################################
# backend/analytics_api/main.py
###############################################
from fastapi import FastAPI
import redis, psycopg2

app = FastAPI()

r = redis.Redis(host='redis', port=6379, db=0)
conn = psycopg2.connect(dbname="events", user="postgres", password="postgres", host="postgres")
cur = conn.cursor()

@app.get("/stats/realtime")
def get_realtime_stats(userId: int):
    count = r.get(f"user:{userId}:actions")
    return {"userId": userId, "actions": int(count) if count else 0}

@app.get("/stats/history")
def get_history_stats(userId: int):
    cur.execute("SELECT COUNT(*) FROM events WHERE userId = %s", (userId,))
    total = cur.fetchone()[0]
    return {"userId": userId, "total_actions": total}

###############################################
# frontend/src/App.js
###############################################
import React from 'react';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div>
      <h1>Realtime Analytics Dashboard</h1>
      <Dashboard />
    </div>
  );
}

export default App;

###############################################
# frontend/src/components/Dashboard.js
###############################################
import React, { useEffect, useState } from 'react';

function Dashboard() {
  const [stats, setStats] = useState({});

  useEffect(() => {
    fetch("http://localhost:8002/stats/realtime?userId=1")
      .then(res => res.json())
      .then(data => setStats(data));
  }, []);

  return (
    <div>
      <h2>User 1 Stats</h2>
      <p>Realtime Actions: {stats.actions}</p>
    </div>
  );
}

export default Dashboard;

###############################################
# docker-compose.yml
###############################################
version: '3'
services:
  zookeeper:
    image: wurstmeister/zookeeper
    ports:
      - "2181:2181"

  kafka:
    image: wurstmeister/kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_ADVERTISED_HOST_NAME: kafka
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: events
    ports:
      - "5432:5432"

  ingestion:
    build: ./backend/ingestion_service
    ports:
      - "8000:8000"

  processor:
    build: ./backend/processor_service

  analytics:
    build: ./backend/analytics_api
    ports:
      - "8002:8002"

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

###############################################
# README.md
###############################################
# Realtime Event Analytics Platform

This project demonstrates a scalable, microservices-based analytics system.

### Features
- Event ingestion via FastAPI
- Stream processing with Kafka
- Caching with Redis
- Storage in PostgreSQL
- Analytics API (FastAPI)
- React dashboard for visualization
- Docker Compose setup

### Run Locally
```bash
docker-compose up --build
```

Visit:
- Ingestion API: http://localhost:8000/docs
- Analytics API: http://localhost:8002/docs
- Dashboard: http://localhost:3000
