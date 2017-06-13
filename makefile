.PHONY: dev unit_test load_test

dev:
	docker-compose up -d
	sleep 3
	docker-compose exec web ./manage.py migrate
	docker-compose logs -f web

unit_test:
	docker-compose run --rm -e DJANGO_SETTINGS_MODULE=settings.base web ./manage.py test tests.test_api

load_test:
	docker-compose -f docker-compose-prod.yml up -d
	sleep 3
	docker-compose -f docker-compose-prod.yml exec web ./manage.py migrate
	docker-compose -f docker-compose-prod.yml exec web ./manage.py shell -c "from tests.create_test_data import main; main(False)"
	docker-compose -f docker-compose-prod.yml -f test.yml run  --rm test
