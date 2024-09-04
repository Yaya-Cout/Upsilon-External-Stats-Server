from external_stats.api.models import ExternalInstallDay
from rest_framework import serializers
from django.db.models import Q

import datetime

class ExternalInstallDaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExternalInstallDay
        fields = ['applications', 'installations', 'wallpaper_count', 'date', 'id']

    def create(self, validated_data):
        """Create or increase stats for the current day."""
        # Get current day
        date = datetime.date.today()

        create_new = False
        data = {
            "applications": {},
            "installations": 0,
            "wallpaper_count": 0,
        }
        try:
            # This code is broken if we go back in the time, but it shouldn't
            # happen in production
            obj = ExternalInstallDay.objects.latest('date')
            if obj.date == date:
                data = {
                    "applications": obj.applications,
                    "installations": obj.installations,
                    "wallpaper_count": obj.wallpaper_count,
                }
            else:
                create_new = True
        except ExternalInstallDay.DoesNotExist:
            create_new = True

        if "applications" in validated_data and isinstance(validated_data["applications"], dict):
            for application in validated_data["applications"]:
                if validated_data["applications"][application] > 0:
                    if application in data["applications"]:
                        data["applications"][application] += 1
                    else:
                        data["applications"][application] = 1
        data["applications"] = dict(sorted(data["applications"].items(), key=lambda item: item[1]))
        data["installations"] += 1

        if "wallpaper_count" in validated_data and validated_data["wallpaper_count"] > 0:
            data["wallpaper_count"] += 1

        if not create_new:
            self.update(obj, data)
        else:
            super().create(data)

        # HACK: To prevent information leak, we are returning data from the day
        # before instead of searching for a real fix for this problem
        return ExternalInstallDay.objects.filter(~Q(date=date)).latest('date')