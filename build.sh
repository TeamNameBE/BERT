git pull
docker-compose up -d --build
docker-compose exec bert poetry run python3 manage.py migrate
