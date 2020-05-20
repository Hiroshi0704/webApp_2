import logging

from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from shiftApp.models import ShiftApp, Worker, WorkSchdule
from shiftApp.serializers import WorkerSerializer, WorkSchduleSerializer

logger = logging.getLogger(__name__)


class WorkerViewSet(viewsets.ModelViewSet):
    """従業員 REST API"""
    serializer_class = WorkerSerializer

    def get_queryset(self):
        shift_app = get_object_or_404(ShiftApp, pk=self.request.user.id)
        return Worker.objects.filter(app=shift_app)


class WorkSchduleViewSet(viewsets.ModelViewSet):
    """勤務予定 REST API"""
    queryset = WorkSchdule.objects.all()
    serializer_class = WorkSchduleSerializer
