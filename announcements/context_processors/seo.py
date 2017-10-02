from django.conf import settings

def seo_context(request):
    return {'GTM_ID': settings.GTM_ID}
