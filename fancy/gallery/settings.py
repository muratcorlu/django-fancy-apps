from django.conf import settings

GALLERY_IMAGE_SIZES = getattr(settings, 'PAGE_TEMPLATES', ("80x80F", "100x100F", "800x600"))
