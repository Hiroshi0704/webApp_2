from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator


class ShiftAppPlan(models.Model):
    """勤務表作成機能登録プラン"""

    title = models.CharField(max_length=150, unique=True)
    price = models.FloatField(validators=[MinValueValidator(0)])
    is_manager = models.BooleanField(default=True)

    def __str__(self):
        return f'[{self.title}] {self.price}'


class ShiftApp(models.Model):
    """勤務表作成機能"""

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    plan = models.ForeignKey(ShiftAppPlan, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return f'ShiftApp [{self.user.username}]'


class WorkPlan(models.Model):
    """1日の勤務計画"""

    title = models.CharField(max_length=150)
    app = models.ForeignKey(ShiftApp, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class WorkStyle(models.Model):
    """勤務形態"""

    symbol = models.CharField(max_length=1)
    start_time = models.TimeField()
    break_time = models.TimeField()
    end_time = models.TimeField()
    is_night = models.BooleanField(default=False)
    app = models.ForeignKey(ShiftApp, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.symbol


class WorkPlanWorkStyleRelation(models.Model):
    """勤務計画と勤務形態を紐付けるクラス
    1日の勤務計画に勤務形態を複数登録（重複あり）するために必要
    """

    work_plan = models.ForeignKey(WorkPlan, on_delete=models.CASCADE)
    work_style = models.ForeignKey(WorkStyle, on_delete=models.CASCADE)
    work_style_num = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'[{self.work_plan.title}] {self.work_style.symbol}: {self.work_style_num}'


class Worker(models.Model):
    """従業員"""

    worker_detail = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    hourlyWage = models.FloatField(validators=[MinValueValidator(0)])
    app = models.ForeignKey(ShiftApp, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.worker_detail.username}'


class Shift(models.Model):
    """勤務表"""

    title = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    worker = models.ManyToManyField(Worker)
    is_public = models.BooleanField(default=False)
    app = models.ForeignKey(ShiftApp, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ShiftPlan(models.Model):
    """勤務表の計画"""

    date = models.DateField()
    work_plan = models.ForeignKey(WorkPlan, on_delete=models.CASCADE, blank=True, null=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)

    def __str__(self):
        if self.work_plan:
            return f'[{self.date}] {self.work_plan.title}'
        else:
            return f'[{self.date}] {self.work_plan}'


class WorkSchdule(models.Model):
    """従業員の勤務予定"""

    date = models.DateField()
    is_rest_request = models.BooleanField(default=False)
    work_style = models.ForeignKey(WorkStyle, on_delete=models.CASCADE, blank=True, null=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.date}] {self.worker}: {self.work_style}'


class ShiftWorkerRelation(models.Model):
    """勤務表と従業員を紐付けるクラス
    従業員の勤務時間を保持するために必要
    """

    total_time = models.FloatField(validators=[MinValueValidator(0)])
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.shift}] {self.worker}: {self.total_time}'
