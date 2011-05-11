import datetime
import cStringIO
import Image
import email
import time

from django.conf import settings
from django.core.mail import mail_managers
from django.template.loader import render_to_string

from celery.decorators import task
from couchdbkit import Server, Consumer

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from core.models import SyncSequenceCache
from core.utils import crop_image_to_dimensions
from record.documents import Record


__copyright__ = "Copyright 2011 Red Robot Studios Ltd."
__license__ = "GPL v3.0 http://www.gnu.org/licenses/gpl.html"


THUMBNAIL_DIMENSIONS = (600, 400)


def get_record_by_id(record_id):
    server = Server(settings.SECURE_COUCHDB_SERVER)
    db = server.get_or_create_db('openelm')
    Record.set_db(db)
    return Record.get(record_id)


def create_thumbnail(photo):
    image = Image.open(photo)
    image = crop_image_to_dimensions(image, THUMBNAIL_DIMENSIONS)
    output = cStringIO.StringIO()
    image.save(output, 'jpeg')
    return output


def process_photo(photo, record):
    if record.source in ('android', 'iphone'):
        image = Image.open(photo)
        if image.size[0] > image.size[1]:
            temp = image.rotate(-90, Image.BILINEAR, expand=True)
            image = cStringIO.StringIO()
            temp.save(image, 'jpeg')
    else:
        image = photo
    headers = {'Content-Type': 'image/jpeg',
        'Expires': '%s GMT' % (email.Utils.formatdate(time.mktime(
                                (datetime.datetime.now() + datetime.timedelta(days=365*2)).timetuple()))),
        'Cache-Control': 'public, max-age=%d' % (3600 * 24 * 365 * 2)}
    conn = S3Connection(settings.S3_CREDENTIALS['access_key'], settings.S3_CREDENTIALS['secret_key'])
    bucket = conn.get_bucket(settings.S3_BUCKET)
    photo_filename = '%s/photo.jpg' % record._id
    key = Key(bucket=bucket, name=photo_filename)
    key.set_contents_from_file(image, headers=headers)
    key.set_acl('public-read')
    thumbnail_filename = '%s/thumbnail.jpg' % record._id
    key = Key(bucket=bucket, name=thumbnail_filename)
    key.set_contents_from_file(create_thumbnail(image), headers=headers)
    key.set_acl('public-read')
    record.photo_url = 'http://%s/%s' % (settings.S3_BUCKET, photo_filename)
    record.thumbnail_url = 'http://%s/%s' % (settings.S3_BUCKET, thumbnail_filename)
    record.save()


@task()
def store_photo_for_record_id(filepath, record_id):
    record = get_record_by_id(record_id)
    photo = open(filepath, 'rb')
    process_photo(photo, record)


@task()
def copy_photo_for_record(record_id):
    record = get_record_by_id(record_id)
    attachments = record._doc.get('_attachments')
    if attachments and 'photo.jpg' in attachments.keys():
        photo = cStringIO.StringIO(record.fetch_attachment('photo.jpg', stream=True).read())
        process_photo(photo, record)
        record.delete_attachment('photo.jpg')


@task()
def delete_photos_for_record_id(record_id):
    conn = S3Connection(settings.S3_CREDENTIALS['access_key'], settings.S3_CREDENTIALS['secret_key'])
    bucket = conn.get_bucket(settings.S3_BUCKET)
    bucket.delete_key('%s/photo.jpg' % record_id)
    bucket.delete_key('%s/thumbnail.jpg' % record_id)


@task()
def send_new_record_email(record_id):
    body = render_to_string('management/email/new_record.txt', {'record_id': record_id})
    mail_managers('New Record Submitted', body)


@task
def compact_couch():
    server = Server(settings.SECURE_COUCHDB_SERVER)
    db = server.get_or_create_db('openelm')
    db.compact()
    db.view_cleanup()


@task()
def process_couchdb_changes():
    server = Server(settings.COUCHDB_SERVER)
    db = server.get_or_create_db('openelm')
    consumer = Consumer(db)
    sequence = SyncSequenceCache.objects.get(pk=1)
    changes = consumer.fetch(filter='record/new_records', since=sequence.last_sequence_id)
    if changes:
        for change in changes['results']:
            record_id = change['id']
            copy_photo_for_record.delay(record_id)
            send_new_record_email.delay(record_id)
        sequence.last_sequence_id = changes['last_seq']
        sequence.save()