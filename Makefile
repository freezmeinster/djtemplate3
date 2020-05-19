run:
	@python manage.py runserver
runplus:
	@python manage.py runserver_plus
runpublic:
	@python manage.py runserver 0.0.0.0:8000
migrate:
	@python manage.py migrate
initdev:
	@python manage.py runscript initdev
builddemo:
	@python manage.py runscript builddemo
initprod:
	@python manage.py runscript initprod
cleanmigrations:
	@python manage.py runscript cleanmigrations
