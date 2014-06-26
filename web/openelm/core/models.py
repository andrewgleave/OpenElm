from django.db import models


__copyright__ = "Copyright 2011-2014 Red Robot Studios Ltd."
__license__ = "MIT http://opensource.org/licenses/MIT"


class SyncSequenceCache(models.Model):
    """Stores the last known sequence id from _changes"""
    last_sequence_id = models.PositiveIntegerField(blank=False, default=0)
    last_sequence_date = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%d - %s' % (self.last_sequence_id, self.last_sequence_date)
