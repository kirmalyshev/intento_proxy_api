build_web:
	docker-compose build --no-cache web

test:
	docker-compose run web pytest test

create_env:
	cp -n envs/dev.env.dist envs/dev.env

up:
	make create_env && docker-compose up web