import os

from django import forms
from couchdbkit.ext.django.forms  import DocumentForm

from record.documents import Record


__copyright__ = "Copyright 2011 Red Robot Studios Ltd."
__license__ = "GPL v3.0 http://www.gnu.org/licenses/gpl.html"


class AddRecordForm(DocumentForm):
    
    MAX_UPLOAD_SIZE = 1024
    ACCEPTED_FILETYPES = ('.jpeg', '.jpg')
    STATUS_CHOICES = (
        ('healthy', 'Healthy'),
        ('inspection-required', 'Inspection Required'))
    
    username = forms.CharField(required=False,
                                label=u'Your username',
                                widget=forms.TextInput(attrs={'placeholder': 'Optional', 'autocomplete': 'on'}),
                                 help_text=u"Use something unique as your username so you can see your contribution to the project")
    photo = forms.ImageField(required=True, help_text=u'Maximum size of 2MB. JPG only.')
    status = forms.ChoiceField(required=True, choices=STATUS_CHOICES)
    location_lat = forms.CharField(required=False, widget=forms.HiddenInput())
    location_lng = forms.CharField(required=False, widget=forms.HiddenInput())
    street_address = forms.CharField(required=False, 
                                        widget=forms.TextInput(attrs={
                                                'placeholder': 'Drag the marker to set the location',
                                                'disabled': 'disabled'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Optional'}))
    #simple honeypot field
    extent = forms.CharField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        document = Record
        exclude = ('photo',)
    
    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo:
            if (photo.size / 2048) > self.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(u'The image is too large to be uploaded. It must be less than 2MB.')
            name, extension = os.path.splitext(photo.name)
            if extension.lower() not in self.ACCEPTED_FILETYPES:
                raise forms.ValidationError(u'We do not support the %s filetype. Please convert your photo ' \
                                            'to a jpeg and try again.' % extension)
        return photo
    
    def clean_extent(self):
        extent = self.cleaned_data['extent']
        if extent:
            raise forms.ValidationError(u'Validation failed.')
        return extent
    
    def clean(self):
        location_lat = self.cleaned_data['location_lat']
        location_lng = self.cleaned_data['location_lng']
        if not location_lat or not location_lng:
            raise forms.ValidationError(u'Please use the map to choose the location ' \
                                        'and edit the street address if necessary')
        return self.cleaned_data


class ManageRecordForm(AddRecordForm):
    
    STATUS_CHOICES = (
        ('healthy', 'Healthy'),
        ('invalid', 'Invalid'),
        ('inspection-required', 'Inspection Required'),
        ('confirmed', 'Confirmed Disease'),
        ('felled', 'Felled'),)
    
    username = forms.CharField(required=False,
                                label=u'Submitter\'s Username',
                                widget=forms.TextInput(attrs={'placeholder': 'Optional', 'autocomplete': 'on'}))
    review_notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Your review notes'}))
    status = forms.ChoiceField(required=False, choices=STATUS_CHOICES)
    photo = forms.ImageField(required=False)
    
    class Meta:
        document = Record
        exclude = ('photo',)