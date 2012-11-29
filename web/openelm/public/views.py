import os

from django.core import urlresolvers
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from record.documents import Record
from record.forms import AddRecordForm
from record.utils import get_couch_document_or_404, get_photo_url_for_record
from record import tasks


__copyright__ = "Copyright 2011 Red Robot Studios Ltd."
__license__ = "GPL v3.0 http://www.gnu.org/licenses/gpl.html"


def submit_report(request):
    if request.method == 'POST':
        form = AddRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            del record.extent
            #remove as we're adding lat/lng as geometry
            del record.location_lat
            del record.location_lng
            record.geometry = {
                'type': 'Point',
                'coordinates': [float(form.cleaned_data['location_lat']),
                                float(form.cleaned_data['location_lng'])]
            }
            record.source = 'web'
            if not record.username:
                record.username = 'anonymous'
            record.save()
            
            filepath = '/tmp/%s.jpg' % (record._id,)
            if os.path.exists(filepath):
                os.remove(filepath)
            #write file to tmp
            photo = open(filepath, 'wb+')
            for chunk in form.cleaned_data['photo'].chunks():
                photo.write(chunk)
            photo.close()
            
            #push the upload off to Celery
            tasks.store_photo_for_record_id.delay(filepath, record._id)
            return HttpResponseRedirect(urlresolvers.reverse('public_submit_done'))
    else:
        form = AddRecordForm()
    return render_to_response('public/submit_report.html',
                {'current_page': 'submit',
                'form': form},
                context_instance=RequestContext(request))

def record_detail(request, record_id):
    record = get_couch_document_or_404(Record, record_id)
    photo_url = get_photo_url_for_record(record)
    return render_to_response('public/record_detail.html',
                {'record': record,
                'photo_url': photo_url,
                'current_page': 'map'},
                context_instance=RequestContext(request))
    