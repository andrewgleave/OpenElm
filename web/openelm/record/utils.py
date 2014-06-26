import os

from django.conf import settings
from django.http import Http404

from couchdbkit import ResourceNotFound


__copyright__ = "Copyright 2011-2014 Red Robot Studios Ltd."
__license__ = "MIT http://opensource.org/licenses/MIT"


REVIEW_ZONE_MAP = {
    'iom': [(54.4337, -4.8272), (54.0307, -4.2791)],
    'se': [(51.102567, -0.548144), (50.7307, 0.781377)]
}


def get_couch_document_or_404(klass, *args, **kwargs):
    try:
        return klass.get(*args, **kwargs)
    except ResourceNotFound:
        raise Http404(u'Record not found')

def get_photo_url_for_record(record):
    if record._doc.get('_attachments'):
        return os.path.join(settings.COUCHDB_ENPOINTS['public'], record._id, u'photo.jpg')
    return u''

def get_review_zone_for_coordinates(lat, lon):
    for k, v in REVIEW_ZONE_MAP.iteritems():
        a, b = v[0], v[1]
        if lat <= a[0] and lat >= b[0] and lon >= a[1] and lon <= b[1]:
            return k
    return None