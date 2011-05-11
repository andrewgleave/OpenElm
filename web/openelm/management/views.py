import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core import urlresolvers
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from record.documents import Record
from record.forms import ManageRecordForm
from record.utils import get_couch_document_or_404, get_photo_url_for_record
from record import tasks


__copyright__ = "Copyright 2011 Red Robot Studios Ltd."
__license__ = "GPL v3.0 http://www.gnu.org/licenses/gpl.html"


RECORDS_PER_PAGE = 20


@login_required
@cache_control(private=True)
def index(request):
    records = Record.view('record/unreviewed', descending=True)
    return render_to_response('management/index.html',
                {'records': records,
                'current_page': 'management'},
                context_instance=RequestContext(request))

@login_required
@cache_control(private=True)
def records(request):
    next = ''
    kwargs = {'descending': True,
            'limit': RECORDS_PER_PAGE + 1}
    if 'n' in request.GET:
        kwargs['startkey'] = request.GET['n']
    records = list(Record.get_db().view('record/all', **kwargs))
    if len(records) > RECORDS_PER_PAGE:
        next = records[-1]['key']
    for record in records:
        record['value']['creation_date'] = convert_datetime_string(record['value']['creation_date'])
        record['value']['review_date'] = convert_datetime_string(record['value'].get('review_date'))
    return render_to_response('management/records.html',
                {'records': records[:-1],
                'next': next,
                'querystring': request.META['QUERY_STRING'],
                'current_page': 'management'},
                context_instance=RequestContext(request))

@login_required
@cache_control(private=True)
def record_detail(request, record_id):
    record = get_couch_document_or_404(Record, record_id)
    photo_url = get_photo_url_for_record(record)
    return render_to_response('management/record_detail.html',
                {'record': record,
                'photo_url': photo_url,
                'current_page': 'management'},
                context_instance=RequestContext(request))

@login_required
@cache_control(private=True)
def edit_record(request, record_id):
    record = get_couch_document_or_404(Record, record_id)
    photo_url = get_photo_url_for_record(record)
    if request.method == 'POST':
        if 'delete' in request.POST:
            record.delete()
            tasks.delete_photos_for_record_id.delay(record_id)
        elif 'approve' in request.POST:
            record.review_date = datetime.datetime.utcnow()
            record.reviewed_by = request.user.username
            record.save()
        else:            
            form = ManageRecordForm(request.POST, instance=record)
            if form.is_valid():
                record = form.save(commit=False)
                record.review_date = datetime.datetime.utcnow()
                record.reviewed_by = request.user.username
                del record.extent
                #remove as we're adding lat/lng as geometry
                del record.location_lat
                del record.location_lng
                record.geometry = {
                    'type': 'Point',
                    'coordinates': [float(form.cleaned_data['location_lat']),
                                    float(form.cleaned_data['location_lng'])]
                }
                record.save()
        return HttpResponseRedirect(urlresolvers.reverse('management_index'))
    else:
        initial = {
            'location_lat': record.geometry['coordinates'][0],
            'location_lng': record.geometry['coordinates'][1]
        }
        form = ManageRecordForm(instance=record, initial=initial)
    return render_to_response('management/edit_record.html',
                {'form': form,
                'photo_url': photo_url,
                'current_page': 'management'},
                context_instance=RequestContext(request))


def convert_datetime_string(value):
    if value:
        value = value.split('.', 1)[0] # strip out microseconds
        value = value[0:19] # remove timezone
        return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
    return ''