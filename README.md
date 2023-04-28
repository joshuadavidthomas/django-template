# django-template

Yet another Django template.

## Getting Started

1. Create a new repository from this template.
2. Find and replace all the instances of `django_project` to your project name.

-   `django_project` -> `your_project_name`
-   `DjangoProject` -> `YourProjectName`

3. Rename the `django_project` directories to your project name.
4. Rename the following in `fly.toml` to your project name, keeping in mind
   it will become your subdomain on fly.io:

-   `app`
-   `env.ALLOWED_HOSTS`
-   `env.CSRF_TRUSTED_ORIGINS`

5. Make sure the `primary_region` in `fly.toml` is the region you want to deploy
   to.
6. Create a new app on [Fly.io](https://fly.io) by running `fly launch` in the
   root of your project. Answer the questions as appropriate, e.g.:

```shell
➜ fly launch
Creating app in /home/.../projects/<example-django_project>
An existing fly.toml file was found for app <example-django_project>.
? Would you like to copy its configuration to the new app? Yes
Scanning source code
Detected a Django app
? Choose an app name (leaving blank will default to '<example-django_project>')
? Select Organization: Example Organization (example-organization)
App will use '...' region as primary
Created app '<example-django_project>' in organization '<example-organization>'
Admin URL: https://fly.io/apps/<example-django_project>
Hostname: <example-django_project>.fly.dev
? Overwrite "/home/.../projects/<example-django_project>/Dockerfile"? No
Set secrets on <example-django_project>: SECRET_KEY
? Would you like to set up a Postgresql database now? Yes
? Select configuration: Development - Single node, 1x shared CPU, 256MB RAM, 1GB disk
? Scale single node pg to zero after one hour? Yes
Creating postgres cluster in organization <example-organization>
...
```

7. Deploy your app by running `fly deploy` in the root of your project. (You may
   need to set the `--local-only` flag if the deploy fails.)
8. Create a superuser by running `fly ssh console` in the root of your project,
   then running `python manage.py createsuperuser` in the console. Alternatively,
   you can run it all in one command:

    `fly ssh console --pty -C 'python /app/manage.py createsuperuser'`

    Note: You will probably need to scale up your VM's memory to run the
    `createsuperuser` command as the default memory is 256MB and seems to be
    insufficient. You can do this by running `fly scale memory 512`.

9. Create a new project in [Sentry](https://sentry.io) and add the DSN URL to
   `env.SENTRY_DSN` in `fly.toml`.

Note: You may need to change `env.DEBUG` to `True` in `fly.toml` to debug
and fix any issues that arise during deployment.
