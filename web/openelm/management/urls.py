from django.conf.urls.defaults import *


__copyright__ = "Copyright 2011 Red Robot Studios Ltd.  All rights reserved."
__license__ = "GPL v3.0 http://www.gnu.org/licenses/gpl.html"


urlpatterns = patterns('',
    url(r'^$', 'management.views.index', name='management_index'),
    url(r'^reports/$', 'management.views.records', name='management_reports'),
    url(r'^record/(?P<record_id>\w+)/$', 'management.views.record_detail', name='management_record_detail'),
    url(r'^record/(?P<record_id>\w+)/edit/$', 'management.views.edit_record', name='management_edit_record'),
)
