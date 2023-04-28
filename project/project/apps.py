from __future__ import annotations

from django.apps import AppConfig


class ProjectConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "project.project"
    label = "github"
    verbose_name = "GitHub"
