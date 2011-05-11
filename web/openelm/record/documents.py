import datetime

from couchdbkit.ext.django.schema import *


__copyright__ = "Copyright 2011 Red Robot Studios Ltd."
__license__ = "GPL v3.0 http://www.gnu.org/licenses/gpl.html"


class Record(Document):
    username = StringProperty(required=True, default='anonymous')
    notes = StringProperty(required=False)
    geometry = DictProperty()
    street_address = StringProperty()
    status = StringProperty(required=True)
    source = StringProperty()
    review_date = DateTimeProperty()
    review_notes = StringProperty(required=False)
    reviewed_by = StringProperty()
    creation_date = DateTimeProperty(default=datetime.datetime.utcnow)

    