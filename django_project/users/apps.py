from __future__ import annotations

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "django_project.users"
    label = "users"
    verbose_name = "Users"
