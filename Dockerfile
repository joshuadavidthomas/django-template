FROM python:3.11-slim-buster as base

ENV PYTHONPATH /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG False

RUN mkdir -p /app

WORKDIR /app


FROM base as py
COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
  && python -m pip install -r requirements.txt


FROM base as app
COPY manage.py /app
COPY django_project /app/django_project
COPY templates /app/templates


FROM node:18-bullseye-slim as node
WORKDIR /app

COPY package.json postcss.config.js tailwind.config.js tsconfig.json vite.config.ts yarn.lock /app/
COPY static/src /app/static/src
RUN yarn install --no-optional \
  && yarn build


FROM app as static
COPY --from=py /usr/local /usr/local
COPY --from=node /app/static/dist /app/static/dist
COPY static/public /app/static/public
RUN DATABASE_URL=sqlite:///db.sqlite3 python manage.py collectstatic --noinput --clear


FROM base as final

COPY --from=py /usr/local /usr/local
COPY --from=app /app /app
COPY --from=static /app/staticfiles /app/staticfiles

RUN addgroup --system django \
  && adduser --system --ingroup django django \
  && chown -R django:django /app

USER django

EXPOSE 8000

CMD ["python", "-m", "gunicorn", "django_project.wsgi:application", "--config", "python:django_project.gunicorn"]
