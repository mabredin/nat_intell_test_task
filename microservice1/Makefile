runserver:
		$(PACKAGE_MANAGER_RUNNER) cd src && uvicorn main:create_app --reload

makemigrations:
		$(PACKAGE_MANAGER_RUNNER) alembic revision --autogenerate -m "${MESSAGE}"

migrate:
		$(PACKAGE_MANAGER_RUNNER) alembic upgrade head

lint:
		$(PACKAGE_MANAGER_RUNNER) black src
		$(PACKAGE_MANAGER_RUNNER) isort src
