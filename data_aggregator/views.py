from locale import locale_alias
from django.http import JsonResponse
from django.http import JsonResponse
from .set_interval import execute, setInterval

inter = None


def activate(request):
    global inter
    if inter != None:
        return JsonResponse({"status": "already activated"})
    else:
        inter = setInterval(1, execute)
        return JsonResponse({"status": "activated"})


def deactivate(request):
    global inter
    if inter != None:
        inter.cancel()
        return JsonResponse({"status": "deactivated"})
    else:
        return JsonResponse({"status": "not activated"})
