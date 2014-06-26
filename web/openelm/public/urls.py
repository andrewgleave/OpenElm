from django.conf.urls.defaults import *


__copyright__ = "Copyright 2011-2014 Red Robot Studios Ltd."
__license__ = "MIT http://opensource.org/licenses/MIT"


urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'public/index.html', 'extra_context': {'current_page':'home'}}, name='public_index'),
    url(r'^about/$', 'django.views.generic.simple.direct_to_template', {'template': 'public/about.html', 'extra_context': {'current_page':'about'}}, name='public_about'),
    url(r'^terms/$', 'django.views.generic.simple.direct_to_template', {'template': 'public/terms.html'},  name='public_terms'),
    url(r'^map/$', 'django.views.generic.simple.direct_to_template', {'template': 'public/map.html', 'extra_context': {'current_page':'map'}}, name='public_map'),
    url(r'^developers/$', 'django.views.generic.simple.direct_to_template', {'template': 'public/developers.html', 'extra_context': {'current_page':'developers'}}, name='public_developers'),
    url(r'^identifying-elms/$', 'django.views.generic.simple.direct_to_template', {'template': 'public/identify.html', 'extra_context': {'current_page':'identify'}}, name='public_identify'),
    url(r'^submit-report/$', 'public.views.submit_report', name='public_submit_report'),
    url(r'^submit-report/done/$', 'django.views.generic.simple.direct_to_template', {'template': 'public/submit_done.html'}, name='public_submit_done'),
    url(r'^record/(?P<record_id>\w+)/$', 'public.views.record_detail', name='public_record_detail'),
)
