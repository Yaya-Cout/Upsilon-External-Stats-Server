from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from django.db.models import Q

import datetime

from external_stats.api.models import ExternalInstallDay
from external_stats.api.serializers import ExternalInstallDaySerializer
from external_stats.api.permissions import IsAdminOrReadOnlyAndPost


class ExternalInstallDayViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows external install days to be viewed or edited.
    """
    # queryset = ExternalInstallDay.objects.all().order_by('-date')
    serializer_class = ExternalInstallDaySerializer
    permission_classes = [IsAdminOrReadOnlyAndPost]

    def get_queryset(self):
        return ExternalInstallDay.objects.filter(~Q(date=datetime.date.today())).all().order_by('-date')