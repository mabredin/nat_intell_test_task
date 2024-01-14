docker-up:
		docker compose up -d

docker-down:
		docker compose down -v
docker-restart:
		docker compose down
		docker image rm test_task_nat_intel-service2:latest
		docker image rm test_task_nat_intel-service1:latest
		docker compose up
