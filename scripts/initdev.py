import sh
import glob
import os
import datetime
from django.conf import settings
from django.core.management import call_command
from django.contrib.auth import get_user_model


User = get_user_model()

def run():
    db_name = settings.DATABASES['default']['NAME']
    if "postgres" in settings.DATABASES['default']['ENGINE']:
        import psycopg2
        try:
            psycopg2.connect("dbname=%s" % db_name)
            print("Deleting DB ...", end="")
            sh.dropdb(db_name)
            print("Done")
        except psycopg2.OperationalError:
            pass
    else:
        if os.path.isfile(db_name):
            os.unlink(db_name)
    print("Done")
    print("Creating DB ...", end="")
    if "postgres" in settings.DATABASES['default']['ENGINE']:
        sh.createdb(db_name)
    print("Done")
    call_command("migrate")
    
    print("Create superuser")
    admin = User.objects.create_superuser(username="admin", password="admin", email="admin@admin.com")


