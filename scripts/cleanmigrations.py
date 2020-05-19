import glob
import os
import shutil
from django.core.management import call_command

def run():
    for item in glob.glob("apps/*/migrations/*"):
        if os.path.isfile(item):
            os.unlink(item)
        else:
            shutil.rmtree(item)
    for it in glob.glob("apps/*/migrations"):
        open(os.path.join(it, "__init__.py"), "a").close()
    call_command("makemigrations")
