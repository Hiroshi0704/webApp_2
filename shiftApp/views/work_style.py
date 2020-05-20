import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from shiftApp.models import ShiftApp, WorkStyle
from shiftApp.serializers import WorkStyleSerializer

logger = logging.getLogger(__name__)


class WorkStyleViewSet(viewsets.ModelViewSet):
    """勤務形態 REST API"""
    serializer_class = WorkStyleSerializer

    def get_queryset(self):
        shift_app = get_object_or_404(ShiftApp, pk=self.request.user.id)
        return WorkStyle.objects.filter(app=shift_app)
