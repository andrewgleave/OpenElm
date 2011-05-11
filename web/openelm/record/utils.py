import os

from django.conf import settings
from django.http import Http404

from couchdbkit import ResourceNotFound


__copyright__ = "Copyright 2011 Red Robot Studios Ltd."
__license__ = "GPL v3.0 http://www.gnu.org/licenses/gpl.html"


def get_couch_document_or_404(klass, *args, **kwargs):
    try:
        return klass.get(*args, **kwargs)
    except ResourceNotFound:
        raise Http404(u'Document not found')

def get_photo_url_for_record(record):
    if record._doc.get('_attachments'):
        return os.path.join(settings.COUCHDB_ENPOINTS['public'], record._id, u'photo.jpg')
    return u''
    