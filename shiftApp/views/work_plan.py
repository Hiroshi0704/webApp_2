import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from shiftApp.models import ShiftApp, WorkPlan, WorkPlanWorkStyleRelation
from shiftApp.serializers import WorkPlanSerializer, WorkPlanWorkStyleRelationSerializer

logger = logging.getLogger(__name__)


class WorkPlanViewSet(viewsets.ModelViewSet):
    """勤務計画 RESR API"""
    serializer_class = WorkPlanSerializer

    def get_queryset(self):
        shift_app = get_object_or_404(ShiftApp, pk=self.request.user.id)
        return WorkPlan.objects.filter(app=shift_app)


class WorkPlanWorkStyleRelationViewSet(viewsets.ModelViewSet):
    """勤務計画と勤務形態関係 RESR API"""
    queryset = WorkPlanWorkStyleRelation.objects.all()
    serializer_class = WorkPlanWorkStyleRelationSerializer
