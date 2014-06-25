from egielda import settings


def site_name_context_processor(request):
    return {'SITE_NAME': getattr(settings, 'SITE_NAME', "e-Giełda")}