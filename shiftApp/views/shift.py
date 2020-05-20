import datetime
import logging
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from rest_framework import generics, views, viewsets
from rest_framework.response import Response

from shiftApp.GenomShiftManager import (GenomShiftConst,
                                        GenomShiftManager, ShiftConfig)
from shiftApp.models import (Shift, ShiftApp, ShiftPlan, ShiftWorkerRelation,
                             WorkSchdule, WorkPlan, WorkStyle, WorkPlanWorkStyleRelation)
from shiftApp.serializers import (ShiftPlanSerializer, ShiftSerializer,
                                  ShiftWorkerRelationSerializer,
                                  WorkerSerializer, WorkSchduleSerializer)

logger = logging.getLogger(__name__)


class ShiftListCreateAPIView(generics.ListCreateAPIView):
    """勤務表一覧・作成 REST API"""
    serializer_class = ShiftSerializer

    def get_queryset(self):
        shift_app = get_object_or_404(ShiftApp, pk=self.request.user.id)
        return Shift.objects.filter(app=shift_app).order_by('updated_at').reverse()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        shift_app = get_object_or_404(ShiftApp, pk=self.request.user.id)
        serializer.save(app=shift_app)


class ShiftRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShiftSerializer

    def get_queryset(self):
        shift_app = get_object_or_404(ShiftApp, pk=self.request.user.id)
        return Shift.objects.filter(app=shift_app)


class ShiftTableDayRangeAPIView(views.APIView):

    def get(self, request, pk, format=None):
        shift_app = get_object_or_404(ShiftApp, pk=request.user.id)
        shift = Shift.objects.filter(app=shift_app, pk=pk).first()
        day_length = (shift.end_date - shift.start_date).days
        day_range = [shift.start_date + datetime.timedelta(days=i) for i in range(day_length - 1)]
        json = {
            'shift': ShiftSerializer(shift).data,
            'day_range': [datetime.datetime.strftime(day, '%Y-%m-%d') for day in day_range],
        }
        return Response(json)


class ShiftTableScheduleAPIView(views.APIView):

    def get(self, request, pk, format=None):
        shift_app = get_object_or_404(ShiftApp, pk=request.user.id)
        shift = Shift.objects.filter(app=shift_app, pk=pk).first()
        day_length = (shift.end_date - shift.start_date).days
        day_range = [shift.start_date + datetime.timedelta(days=i) for i in range(day_length - 1)]
        json = []
        for worker in shift.worker.all():
            json_detail = {'worker': WorkerSerializer(worker).data}
            schedule = {str(day): WorkSchduleSerializer(WorkSchdule.objects.get_or_create(worker=worker, date=day, shift=shift)[0]).data for day in day_range}
            json_detail.update(schedule)
            json.append(json_detail)

        return Response(json)


class ShiftPlanViewSet(viewsets.ModelViewSet):
    """勤務表の計画 REST API"""
    queryset = ShiftPlan.objects.all()
    serializer_class = ShiftPlanSerializer


class ShiftWorkerRelationViewSet(viewsets.ModelViewSet):
    """勤務表と従業員関係 REST API"""
    queryset = ShiftWorkerRelation.objects.all()
    serializer_class = ShiftWorkerRelationSerializer


class ShiftInputView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        return HttpResponse('hello')

    def post(self, request, pk, *args, **kwargs):
        app = get_object_or_404(ShiftApp, pk=self.request.user.id)
        shift = get_object_or_404(Shift, pk=pk, app=app)

        def get_day_range(shift_obj):
            diff = (shift_obj.end_date - shift_obj.start_date).days
            return [shift_obj.start_date + datetime.timedelta(days=i) for i in range(diff + 1)]
        day_range = get_day_range(shift)
        day_length = len(day_range)
        workers = shift.worker.all()
        work_plans = WorkPlan.objects.filter(app=app)
        work_styles = WorkStyle.objects.filter(app=app)
        # {worker: [sche, sche, sche]}
        work_sche_dict = {
            worker: [WorkSchdule.objects.get_or_create(
                worker=worker, date=day, shift=shift)[0] for day in day_range] for worker in workers
        }
        rest_types = [GenomShiftConst.REST_TYPE]
        night_types = [style.id for style in work_styles if style.is_night]
        shift_pattern_dict = {}
        for plan in work_plans:
            symbols = []
            for plan_detail in WorkPlanWorkStyleRelation.objects.filter(work_plan=plan):
                symbols += [plan_detail.work_style.id] * plan_detail.work_style_num
            shift_pattern_dict[plan.id] = symbols
            shift_pattern_dict[plan.id] += [GenomShiftConst.REST_TYPE] * max(0, len(workers) - len(shift_pattern_dict[plan.id]))
            shift_pattern_dict[plan.id] = shift_pattern_dict[plan.id][:len(workers)]

        def get_work_time(work_style):
            end = datetime.datetime.combine(datetime.date.today(), work_style.end_time)
            start = datetime.datetime.combine(datetime.date.today(), work_style.start_time)
            break_time = work_style.break_time
            break_time_included = start + datetime.timedelta(hours=break_time.hour, minutes=break_time.minute, seconds=break_time.second)
            return max(0.0, (end - break_time_included).total_seconds() / 60 / 60)
        work_type_time = {work_style.id: get_work_time(work_style) for work_style in work_styles}
        rest_requests = [[j for j, sche in enumerate(work_sche_dict[worker]) if sche.is_rest_request] for i, worker in enumerate(workers)]
        shift_plans = [ShiftPlan.objects.get_or_create(shift=shift, date=day)[0] for day in day_range]
        shift_pattern = [shift_detail.work_plan.id if shift_detail.work_plan else random.choice(list(shift_pattern_dict.keys())) for shift_detail in shift_plans]

        params = {
            'day_length': day_length,
            'max_work_day': 6,
            'rest_type': rest_types,
            'night_type': night_types,
            'work_type_time': work_type_time,
            'shift_pattern_dict': shift_pattern_dict,
            'rest_requests': rest_requests,
            'shift_pattern': shift_pattern,
            'debug': True
        }
        shift_config = ShiftConfig(**params)
        genom_shift_manager = GenomShiftManager(shift_config)
        best = genom_shift_manager.execute()
        h_shift = best.get_h_shift()
        for i, worker in enumerate(workers):
            for j, date in enumerate(day_range):
                work_style_id = h_shift[i][j]
                defaults = {'work_style': None}
                if work_style_id != GenomShiftConst.REST_TYPE:
                    defaults['work_style'] = WorkStyle.objects.get(id=work_style_id)
                WorkSchdule.objects.update_or_create(
                    worker=worker,
                    shift=shift,
                    date=date,
                    defaults=defaults
                )

        result = {'success': True}
        return JsonResponse(result)
