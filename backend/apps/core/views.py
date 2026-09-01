from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET


@never_cache
@require_GET
def health_check(request):
    """Return a dependency-free liveness response for the internal proxy."""
    return JsonResponse({"status": "ok", "service": "postgraduate-studies"})
