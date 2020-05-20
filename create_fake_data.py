from faker import Factory
import django
import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()
faker_ja = Factory.create('ja_JP')
faker_en = Factory.create()


def create_user(num):
    from accounts.models import CustomUser

    if len(CustomUser.objects.all()) >= 10:
        return

    for i in range(num):
        username = faker_en.name()
        email = faker_en.safe_email()
        password = 'Passowrd01'
        CustomUser.objects.get_or_create(username=username, email=email, password=password)


def create_shift_app(num):
    from accounts.models import CustomUser
    from shiftApp.models import ShiftApp, ShiftAppPlan

    if len(ShiftApp.objects.all()) >= 5:
        return

    random_user = random.sample(list(CustomUser.objects.all()), num)
    for user in random_user:
        ShiftApp.objects.get_or_create(user=user, plan=ShiftAppPlan.objects.first())


def create_worker(num):
    from shiftApp.models import Worker, ShiftApp

    if len(Worker.objects.all()) >= 8:
        return

    random_app = random.sample(list(ShiftApp.objects.all()), num)
    random_user = [app.user for app in random_app]

    for user in random_user:
        Worker.objects.get_or_create(worker_detail=user, hourlyWage=1000, app=random.choice(list(ShiftApp.objects.all())))


def create_shift(num):
    from shiftApp.models import Shift, ShiftApp

    shift_apps = ShiftApp.objects.all()

    if len(Shift.objects.all()) >= 30:
        return

    for i in range(num):
        app = random.choice(list(shift_apps))
        user = app.user
        app_ = ShiftApp.objects.filter(user=1).first()
        Shift.objects.get_or_create(
            title=faker_en.file_name(),
            start_date=faker_en.date_this_year(),
            end_date=faker_en.date_this_year(),
            app=app_,
        )


if __name__ == "__main__":
    create_user(9)
    create_shift_app(5)
    create_worker(5)
    create_shift(20)
