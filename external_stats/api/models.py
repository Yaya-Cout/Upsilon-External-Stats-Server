import datetime
from django.db import models


# We have chosen to aggregate stats by day instead of tracking each user
# separately to avoid privacy problems
class ExternalInstallDay(models.Model):
    """A single install in database."""
    # List of applications and their installations stats as JSON (easier to use)
    applications = models.JSONField()

    # Total number of installation (increased by one each request)
    installations = models.IntegerField(default=0)

    # Wallpaper count
    wallpaper_count = models.IntegerField(default=0)

    # Date
    date = models.DateField(default=datetime.date.today)

    # We are not logging the number of files as it seems useless as we can't
    # associate it with a specific application and an average is not useful


class SuccessfulExternalInstallDay(ExternalInstallDay):
    pass
