
.prepare:
	pip3 install pipenv
	pipenv install

.build:
	docker build -t syrics.us/patroni/cluster ./docker/patroni
	docker build -t syrics.us/patroni/gateway ./docker/gateway

network:
	docker network create crosssite

primary: .prepare .build
	python3 make.py cluster --name primary
	docker-compose -p "syrics.us - patroni/primary" -f build/docker-compose-primary.yml up

secondary: .prepare .build
	python3 make.py cluster --name secondary
	docker-compose -p "syrics.us - patroni/secondary" -f build/docker-compose-secondary.yml up

prune-containers:
	docker system prune --all

prune-images:
	docker image prune --all

clean-compose:
	docker-compose -f build/docker-compose-primary.yml rm -sf
	docker-compose -f build/docker-compose-secondary.yml rm -sf

clean-containers:
	$(foreach container_id,$(shell docker ps -f name=patroni -aq),docker stop $(container_id); docker rm -f $(container_id);)
	if [ $(shell docker images | grep "patroni") ]; then \
	  docker images | grep "patroni" | awk '{print $$3}' | xargs docker rmi --force; \
	fi

clean-volumes: clean
	docker volume rm patroni_volume

clean: clean-compose clean-containers clean-volumes
	rm -rf build