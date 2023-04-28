from __future__ import annotations

from django.apps import AppConfig


class DjangoProjectConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "django_project.django_project"
    label = "github"
    verbose_name = "GitHub"
