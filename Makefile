up:
	docker compose -f docker-compose_db.yml up -d
up_build:
	docker compose -f docker-compose_db.yml up --build

down:
	docker compose -f docker-compose_db.yml down
down_net:
	docker compose -f docker-compose_db.yml down && docker network prune --force


alembic_revision:
    alembic revision --autogenerate
alembic_upgrade:
    alembic upgrade head

app_start:
    uvicorn main:app --reload


