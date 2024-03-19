import schedule
import typer
import asyncio
import subprocess
from pathlib import Path
from main.main import create_dev_app
from main.db import async_main
from admin.models import User, EndPoints, App, JWTSalt, Page as SinglePage, Role, Feature
from main.helper import update_jwt, generate_endpoints_json, clear_log_files

path = Path(__file__).parent
capp = typer.Typer()
app = create_dev_app()


# while True:
generate_endpoints_json()
schedule.every(60).minutes.do(update_jwt)
schedule.every(60).minutes.do(generate_endpoints_json)
schedule.every(15).seconds.do(clear_log_files)


@capp.command()
def rung():
    """starts gunicorn server of the app with uvicorn works bound  to 0.0.0.0:9000 with one worker
    """
    #  to make ssl keys
    # openssl genrsa 4096 > ssl.key

    # openssl req -new -x509 -nodes -sha1 -days 365 -key ssl.key > ssl.cert
    subprocess.run(["gunicorn", "manage:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:9500", "--reload",
                    "-w", "1"])


@capp.command()
def runh():
    """starts gunicorn server of the app with uvicorn works bound  to 0.0.0.0:9000 with one worker
    """
    subprocess.run(["hypercorn", "manage:app", "-b", "0.0.0.0:9500", "--reload",
                    "-w", "2", "--keyfile", "ssl.key", "--certfile", "ssl.cert"])


@capp.command()
def rund():
    """starts gunicorn server of the app with uvicorn works bound  to 0.0.0.0:9000 with one worker
    """
    subprocess.run(["daphne", "manage:app", "-b", "0.0.0.0:9500", "--reload",
                    "-w", "1", "--keyfile", "ssl.key", "--certfile", "ssl.cert"])


@capp.command()
def rungr():
    """starts gunicorn server of the app with uvicorn works bound  to 0.0.0.0:9000 with one worker
    """

    subprocess.run(["granian", "--interface", "asgi", "manage:app", "--host", "0.0.0.0", "--port", "9500", "--reload",
                    "--workers", "1", "--ssl-keyfile", "ssl.key", "--ssl-certificate", "ssl.cert"])


@capp.command()
def upgrade():
    """creates  base models based on their metadata"""
    asyncio.run(async_main())


@capp.command()
def migratenew():
    from main.db import engine
    # RouteResponse.metadata.create_all(bind=engine)
    # RouteResponseRoles.metadata.create_all(bind=engine)
    # Page.metadata.create_all(bind=engine)
    # PageRoutes.metadata.create_all(bind=engine)
    # UsersPage.metadata.create_all(bind=engine)
    # Banks.metadata.create_all(bind=engine)
    # HrFileType.metadata.create_all(bind=engine)

    print('Worked')


@capp.command()
def scheduled():
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    capp()
