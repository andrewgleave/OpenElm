import re
import string

from django import template
from django.template.defaultfilters import stringfilter


__copyright__ = "Copyright 2011-2014 Red Robot Studios Ltd."
__license__ = "MIT http://opensource.org/licenses/MIT"


STRIP_PUNCTUATION_REGEX = re.compile('[%s]' % re.escape(string.punctuation))

register = template.Library()

@register.filter
@stringfilter
def strip_punctuation(value):
    return STRIP_PUNCTUATION_REGEX.sub(' ', value)