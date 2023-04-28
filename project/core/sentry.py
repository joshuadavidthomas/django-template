from __future__ import annotations


def sentry_traces_sampler(sampling_context):
    """
    Returns an int representing the probability of a trace being sampled.

    Disregards any health check requests.
    """
    DISGARDED_METHODS = ["GET", "HEAD"]
    DISGARDED_PATHS = ["/up/"]

    if (
        sampling_context.get("wsgi_environ", None)
        and sampling_context["wsgi_environ"]["REQUEST_METHOD"] in DISGARDED_METHODS
        and sampling_context["wsgi_environ"]["PATH_INFO"] in DISGARDED_PATHS
    ):
        return 0

    return 0.5
