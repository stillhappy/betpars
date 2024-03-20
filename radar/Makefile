run:
	docker-compose up -d --build

stop:
	docker-compose stop

del_app_c:
	docker rm my_project_pars

del_app_i:
	docker rmi postgres-app

del_all_c:
	docker rm my_project_pars portainer postgres pgadmin4

del_all_i:
	docker rmi postgres-app portainer/portainer-ce:latest dpage/pgadmin4 postgres

del_all_v:
	docker volume rm postgres_pgadmin_data postgres_postgres_data