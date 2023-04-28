from __future__ import annotations

from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET
from sentry_sdk import last_event_id


def custom_error_404(request, exception=None, *args, **kwargs):
    response = render(request, "404.html", context={}, status=404)
    return response


def custom_error_500(request, *args, **kwargs):
    response = render(
        request, "500.html", context={"sentry_event_id": last_event_id()}, status=500
    )
    return response


@require_GET
def robots_txt(request):
    return render(request, "robots.txt", content_type="text/plain")


@require_GET
def security_txt(request):
    return render(
        request,
        ".well-known/security.txt",
        context={
            "year": timezone.now().year + 1,
        },
        content_type="text/plain",
    )
