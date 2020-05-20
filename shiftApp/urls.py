from django.urls import include, path
from rest_framework import routers

from .views import shift, shift_app, work_plan, work_style, worker

router = routers.DefaultRouter()
# router.register('shift', shift.ShiftViewSet)
router.register('work_plan', work_plan.WorkPlanViewSet, 'workPlan')
router.register('work_plan_work_style_relation', work_plan.WorkPlanWorkStyleRelationViewSet)
router.register('work_style', work_style.WorkStyleViewSet, 'workStyle')
router.register('worker', worker.WorkerViewSet, 'worker')
router.register('work_schedule', worker.WorkSchduleViewSet)

app_name = 'shiftApp'
urlpatterns = [
    path('registration/', shift_app.ShiftAppRegistrationView.as_view(), name='registration'),
    path('update/<int:pk>/', shift_app.ShiftAppUpdateView.as_view(), name='update'),
    path('cancellation/', shift_app.ShiftAppCancellationView.as_view(), name='cancellation'),
    path('', shift_app.ShiftAppHomeView.as_view(), name='home'),
    path('setting/', shift_app.ShiftAppSettingView.as_view(), name='setting'),
    path('ajax/', include(router.urls)),
    path('shift/', shift.ShiftListCreateAPIView.as_view()),
    path('shift/<int:pk>/', shift.ShiftRetrieveUpdateDestroyAPIView.as_view()),
    path('shift/table/day_range/<int:pk>/', shift.ShiftTableDayRangeAPIView.as_view()),
    path('shift/table/schedule/<int:pk>/', shift.ShiftTableScheduleAPIView.as_view()),
    path('shift/input/<int:pk>/', shift.ShiftInputView.as_view(), name='shift_input'),
]
