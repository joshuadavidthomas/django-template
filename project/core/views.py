from __future__ import annotations

from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET


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
