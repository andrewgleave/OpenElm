import re
import string

from django import template
from django.template.defaultfilters import stringfilter


__copyright__ = "Copyright 2011 Red Robot Studios Ltd."
__license__ = "GPL v3.0 http://www.gnu.org/licenses/gpl.html"


STRIP_PUNCTUATION_REGEX = re.compile('[%s]' % re.escape(string.punctuation))

register = template.Library()

@register.filter
@stringfilter
def strip_punctuation(value):
    return STRIP_PUNCTUATION_REGEX.sub(' ', value)