import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from shiftApp.models import ShiftApp

logger = logging.getLogger(__name__)


class AppListView(LoginRequiredMixin, View):
    """アプリケーション一覧画面"""

    def get(self, request, *args, **kwargs):
        # 機能リスト 機能名: 使用可否:
        app_list = [
            {
                'name': 'shiftApp',
                'enable': ShiftApp.objects.filter(user=request.user).exists(),
                'open_url': reverse('shiftApp:home'),
                'buy_url': reverse('shiftApp:registration'),
                'delete_url': reverse('shiftApp:cancellation'),
            },
            {'name': 'newsApp', 'enable': False},
            {'name': 'bookingApp', 'enable': True},
        ]
        context = {
            'app_list': app_list
        }
        return render(request, 'pages/app_list.html', context)
