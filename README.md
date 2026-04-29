# Flask Task Manager

A REST API for managing tasks — built as part of a DevOps end-to-end project.

## Tech Stack
- Python 3 + Flask
- Containerized with Docker
- CI/CD via Jenkins
- Deployed on Kubernetes
- Monitored with Prometheus + Grafana

## Run locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | /tasks | List all tasks |
| GET | /tasks/:id | Get one task |
| POST | /tasks | Create task |
| PUT | /tasks/:id | Update task |
| DELETE | /tasks/:id | Delete task |
