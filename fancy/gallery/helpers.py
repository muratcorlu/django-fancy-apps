import uuid, os
from settings import GALLERY_ENCRYPT_FILENAMES, GALLERY_DIR
from datetime import datetime
from fancy.utils import slugify
import hashlib

def get_upload_path(instance, filename):
    parts = filename.split('.')
    ext = parts[-1]
    parts.pop()
    basename = '.'.join(parts)

    today = datetime.now()
    
    if GALLERY_ENCRYPT_FILENAMES:
        time_string = today.strftime("%H-%M-%S")
        hash = hashlib.sha224( "%s-%s" % (filename, time_string) ).hexdigest()
        path = os.path.join(GALLERY_DIR, "%s/%s/%s.%s" % (hash[:2], hash[2:4], hash, ext.lower()) )
    else:
        date_path = today.strftime("%Y/%m")
        
        path = os.path.join(GALLERY_DIR, date_path, "%s.%s" % (slugify(basename), ext.lower()))
        
    return path
