docker network create myNetwork

docker run --name library_db \
    -p 6432:5432 \
    -e POSTGRES_USER=qwerty \ 
    -e POSTGRES_PASSWORD=qwerty \ 
    -e POSTGRES_DB=library \
    -e PGTZ=Europe/Berlin \
    --network=myNetwork \
    --volume pg-library-data:/var/lib/postgresql/data \
    -d postgres:17

docker run --name library_cache 
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4

docker run --name library_back \
    -p 8888:8000 \
    --network=myNetwork \
    library_image

docker run --name library_celery_worker
    --network=myNetwork \
    library_image \
    celery --app=src.task.celery_app:celery_instance worker -l INFO

docker build -t library_image .