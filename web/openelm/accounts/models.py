from django.contrib.auth.models import User


__copyright__ = "Copyright 2011-2014 Red Robot Studios Ltd."
__license__ = "MIT http://opensource.org/licenses/MIT"


class UserProfile(models.Model):
    
    REVIEW_ZONES = (
        ('iom', 'Isle of Man'),
        ('se', 'South East')
    )
    
    user = models.OneToOneField(User)
    review_zone = models.CharField(blank=False, max_length=3, choices=REVIEW_ZONES)
