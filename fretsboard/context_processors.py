from django.conf import settings


def piwik_code(request):
    piwik_info = {
        'PIWIK_URL': getattr(settings, 'PIWIK_URL', ''),
        'PIWIK_SITE_ID': getattr(settings, 'PIWIK_SITE_ID', ''),
    }
    return piwik_info
