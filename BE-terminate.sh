# Docker compose container down
docker-compose -f docker-compose.backend.yml down

# Docker compose db remove
docker-compose -f docker-compose.backend.yml down --volumes

# Docker image remove
docker image rm aira_v2_be-backend 