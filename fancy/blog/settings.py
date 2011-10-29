from django.conf import settings

FEED_TITLE = getattr(settings, 'FEED_TITLE', 'Site Title')
FEED_LINK = getattr(settings, 'FEED_LINK', 'http://www.example.com')
FEED_DESCRIPTION = getattr(settings, 'FEED_DESCRIPTION', 'Site Description')
