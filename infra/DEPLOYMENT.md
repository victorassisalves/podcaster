# Deployment Instructions (GCP)

## 1. Setup GCP Project
- Create a new project in Google Cloud Console.
- Enable APIs: Cloud Run, Artifact Registry, Firestore, Cloud Storage, Vertex AI.

## 2. Infrastructure for POC (Cheapest Option)
For a cost-effective POC:
- **Frontend & API**: Use **Google Cloud Run**.
- **LiveKit Server**: Use a **Compute Engine (e2-medium)** instance.
- **Agents**: Can run on the same Compute Engine instance or a separate Cloud Run job (if configured for long-running connections).

### LiveKit Setup (VM)
1. Provision a VM with a public IP.
2. Install Docker.
3. Use the LiveKit official docker-compose setup to launch the server.

## 3. Deployment Steps

### Backend (Cloud Run)
```bash
gcloud auth configure-docker
docker build -t gcr.io/[PROJECT_ID]/podcaster-backend ./backend
docker push gcr.io/[PROJECT_ID]/podcaster-backend
gcloud run deploy podcaster-backend --image gcr.io/[PROJECT_ID]/podcaster-backend --env-vars-file .env.yaml
```

### Frontend (Cloud Run)
```bash
docker build -t gcr.io/[PROJECT_ID]/podcaster-frontend ./frontend
docker push gcr.io/[PROJECT_ID]/podcaster-frontend
gcloud run deploy podcaster-frontend --image gcr.io/[PROJECT_ID]/podcaster-frontend
```

## 4. Environment Variables
Ensure you set the following in Cloud Run and the VM:
- `GOOGLE_API_KEY`
- `LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `GCS_BUCKET_NAME`
