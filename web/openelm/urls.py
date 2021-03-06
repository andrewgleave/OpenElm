from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


__copyright__ = "Copyright 2011 Red Robot Studios Ltd."
__license__ = "GPL v3.0 http://www.gnu.org/licenses/gpl.html"


admin.autodiscover()


urlpatterns = patterns('',
    (r'', include('openelm.public.urls')),
    (r'accounts/', include('openelm.accounts.urls')),
    (r'management/', include('openelm.management.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # Serve media files through dev server.
    urlpatterns += patterns('',
        (r'^media/(v\d*/)?(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
