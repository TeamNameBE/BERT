git pull
docker-compose up -d --build
docker-compose exec bert python3 manage.py migrate
