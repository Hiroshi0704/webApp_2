from django.urls import path

from . import views

app_name = 'pages'
urlpatterns = [
    path('app/list/', views.AppListView.as_view(), name='app_list'),
]
