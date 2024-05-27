# Run AI-talent

```
cd python
docker-compose up -d --build
```

# Run chat

curl -X POST http://localhost:8000/chat \
 -H "Content-Type: application/json" \
 --data '{"text":"ここにテキスト"}'

# Stop AI-talent

```
docker-compose down
```

# Deploy to Azure container registry

```
cd python
az login
az acr login --name washbasin2849
docker buildx build --platform linux/amd64 -t washbasin2849.azurecr.io/talent-talk:v1.0.2 -f Dockerfile --push .
```

# Pull from Azure container registry

```
cd workspaces
docker stop talent-talk
docker rm talent-talk

docker pull washbasin2849.azurecr.io/talent-talk:v1.0.2
docker run --rm -d -p 8000:8000 --env-file .env --name talent-talk --gpus all washbasin2849.azurecr.io/talent-talk:v1.0.2
docker logs -f talent-talk
```
