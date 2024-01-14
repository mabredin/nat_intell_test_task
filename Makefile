docker-up:
		docker compose up -d

docker-down:
		docker compose down -v
docker-restart:
		docker compose down -v
		docker image rm def1ner/ethereum-service-grpc:latest
		docker image rm def1ner/voting-service-grpc:latest
		docker compose up -d
docker-finish:
		docker compose down -v
		docker image rm def1ner/ethereum-service-grpc:latest
		docker image rm def1ner/voting-service-grpc:latest

