from rest_framework import serializers

from accounts.models import CustomUser

from .models import (Shift, ShiftApp, ShiftAppPlan, ShiftPlan,
                     ShiftWorkerRelation, Worker, WorkPlan,
                     WorkPlanWorkStyleRelation, WorkSchdule, WorkStyle)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class ShiftAppPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftAppPlan
        fields = ['title', 'price', 'is_manager']


class ShiftAppSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    plan = ShiftAppPlanSerializer()

    class Meta:
        model = ShiftApp
        fields = ['id', 'user', 'plan']


class WorkerSerializer(serializers.ModelSerializer):
    worker_detail = UserSerializer()

    class Meta:
        model = Worker
        fields = ['id', 'worker_detail', 'hourlyWage', 'app']


class ShiftSerializer(serializers.ModelSerializer):
    worker_info = WorkerSerializer(many=True, read_only=True, source='worker')
    worker = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Worker.objects.all())
    app = ShiftAppSerializer(read_only=True)

    class Meta:
        model = Shift
        fields = ['id', 'title', 'start_date', 'end_date', 'created_at', 'updated_at', 'worker', 'worker_info', 'is_public', 'app']


class WorkPlanSerializer(serializers.ModelSerializer):
    app = ShiftAppSerializer()

    class Meta:
        model = WorkPlan
        fields = ['id', 'title', 'app']


class WorkStyleSerializer(serializers.ModelSerializer):
    app = ShiftAppSerializer()

    class Meta:
        model = WorkStyle
        fields = ['id', 'symbol', 'start_time', 'break_time', 'end_time', 'is_night', 'app']


class WorkPlanWorkStyleRelationSerializer(serializers.ModelSerializer):
    work_plan = WorkPlanSerializer()
    work_style = WorkStyleSerializer()

    class Meta:
        model = WorkPlanWorkStyleRelation
        fields = ['id', 'work_plan', 'work_style', 'work_style_num']


class WorkSchduleSerializer(serializers.ModelSerializer):
    shift = ShiftSerializer()
    work_style = WorkStyleSerializer()

    class Meta:
        model = WorkSchdule
        fields = ['id', 'date', 'is_rest_request', 'work_style', 'worker', 'shift']


class ShiftPlanSerializer(serializers.ModelSerializer):
    work_plan = WorkPlanSerializer()
    shift = ShiftSerializer()

    class Meta:
        model = ShiftPlan
        fields = ['id', 'date', 'work_plan', 'shift']


class ShiftWorkerRelationSerializer(serializers.ModelSerializer):
    shift = ShiftSerializer()
    worker = WorkerSerializer()

    class Meta:
        model = ShiftWorkerRelation
        fields = ['id', 'total_time', 'shift', 'worker']
