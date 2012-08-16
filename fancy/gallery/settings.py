from django.conf import settings

GALLERY_DIR = getattr(settings, 'GALLERY_DIR', "gallery")
GALLERY_ORIGINAL_IMAGESIZE = getattr(settings, 'GALLERY_ORIGINAL_IMAGESIZE', "1600x1200")
GALLERY_ENCRYPT_FILENAMES = getattr(settings, 'GALLERY_ENCRYPT_FILENAMES', False)