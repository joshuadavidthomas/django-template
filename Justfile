##################
#  DEPENDENCIES  #
##################

pip-compile *ARGS:
    pip-compile --resolver=backtracking {{ ARGS }} --generate-hashes requirements.in

install:
    python -m pip install --upgrade -r requirements.txt

pup:
    python -m pip install --upgrade pip pip-tools

update:
    @just pup
    @just pip-compile --upgrade
    @just install

##################
#     DJANGO     #
##################

manage *COMMAND:
    python -m manage {{ COMMAND }}

dev PORT="8000":
    @just manage runserver 0.0.0.0:{{ PORT }}

adev PORT="8000":
    python -m uvicorn --reload --host 0.0.0.0 --port {{ PORT }} project.asgi:application

prod:
    python -m gunicorn project.wsgi:application --config python:project.gunicorn

aprod:
    python -m gunicorn project.asgi:application -k uvicorn.workers.UvicornWorker --config python:project.gunicorn

alias mm := makemigrations

makemigrations *APPS:
    @just manage makemigrations {{ APPS }}

migrate *ARGS:
    @just manage migrate {{ ARGS }}

shell:
    @just manage shell_plus

##################
#     DOCKER     #
##################

enter CONTAINER="django-application-template[-_]devcontainer[-_]app" SHELL="zsh" WORKDIR="/workspaces/django-application-template" USER="vscode":
    #!/usr/bin/env sh
    if [ -f "/.dockerenv" ]; then
        echo "command cannot be run from within a Docker container"
    else
        case {{ SHELL }} in
            "zsh" )
                shell_path="/usr/bin/zsh" ;;
            "bash" )
                shell_path="/bin/bash" ;;
            "sh" )
                shell_path="/bin/sh" ;;
            * )
                shell_path="/usr/bin/zsh" ;;
        esac

        container=$(docker ps --filter "name={{ CONTAINER }}" --format "{{{{.Names}}")

        docker exec -it -u {{ USER }} -w {{ WORKDIR }} $container $shell_path
    fi
