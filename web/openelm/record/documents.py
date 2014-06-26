import datetime

from couchdbkit.ext.django.schema import *


__copyright__ = "Copyright 2011-2014 Red Robot Studios Ltd."
__license__ = "MIT http://opensource.org/licenses/MIT"


class Record(Document):
    username = StringProperty(required=False, default='anonymous')
    notes = StringProperty(required=False)
    geometry = DictProperty()
    street_address = StringProperty()
    status = StringProperty(required=True)
    source = StringProperty()
    review_date = DateTimeProperty()
    review_notes = StringProperty(required=False)
    reviewed_by = StringProperty()
    review_zone = StringProperty()
    creation_date = DateTimeProperty(default=datetime.datetime.utcnow)

    