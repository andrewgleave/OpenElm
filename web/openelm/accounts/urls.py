from django.conf.urls.defaults import *


__copyright__ = "Copyright 2011 Red Robot Studios Ltd."
__license__ = "GPL v3.0 http://www.gnu.org/licenses/gpl.html"


urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='accounts_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logout.html'}, name='accounts_logout'),
)
