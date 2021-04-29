# Stationery-shop-v02-with-Docker

## Project ready to launch, all you need to do, is

clone repository

navigate to project directory
```
cd Stationery-shop-v02-with-Docker
```
build containers
```
docker-compose -f docker_compose/docker-compose.prod01.yaml up -d --build
```
wait till it's done

apply migrations
```
docker-compose -f docker_compose/docker-compose.prod01.yaml exec web python manage.py migrate --noinput
```
Create pg_trgm extension

connect to postgres container
```
docker exec -it <container ID> or <container name> /bin/sh
```
connect to DB as DB user
```
psql -d super_shop_db_prod -U  shop_user -W
```
create extension pg_trgm for search
```
CREATE EXTENSION pg_trgm;
```
api endpoints:

your domain/en/api/shop/categories/

your domain/en/api/shop/products/

your domain/en/api/shop/products/<product_id>/

your domain/en/api/orders/order_list/

## Remember, if you want to use this build in production, change values in env_files/.env.prod and env_files/.env.prod.db, because current values just for test, do not expose your .env files to anyone.
