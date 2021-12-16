default: build deploy

build:
	docker-compose build

deploy:
	docker stack rm flask
	sleep 10
	docker stack deploy -c docker-compose-stack.yml flask