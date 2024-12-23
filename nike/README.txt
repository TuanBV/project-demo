# Run docker
docker-compose up --build

# Delete cache build in docker compose
docker-compose build --no-cache

# Delete image build
docker image prune -a

# Delete cache and folder
docker system prune -a --volumes

# Stop and delete container, network, volumes
docker-compose down --volumes --remove-orphans
