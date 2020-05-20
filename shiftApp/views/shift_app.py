import logging

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, View
from django.views.generic.edit import DeleteView

from shiftApp.forms import ShiftAppRegistrationForm
from shiftApp.models import ShiftApp, ShiftAppPlan


logger = logging.getLogger(__name__)


class ShiftAppRegistrationView(LoginRequiredMixin, TemplateView):
    """勤務表作成機能登録画面"""
    template_name = 'shiftApp/registration.html'

    def get(self, request, *args, **kwargs):
        if ShiftApp.objects.filter(user=request.user).exists():
            return redirect('shiftApp:home')

        shift_app_plans = ShiftAppPlan.objects.all()
        shift_app_plan_titles = [obj.title for obj in shift_app_plans]
        shift_app_plan_prices = [obj.price for obj in shift_app_plans]
        context = {
            'form': ShiftAppRegistrationForm(),
            'shift_app_plan_titles': shift_app_plan_titles,
            'shift_app_plan_prices': shift_app_plan_prices,
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = ShiftAppRegistrationForm(request.POST)
        shift_app_plans = ShiftAppPlan.objects.all()
        shift_app_plan_titles = [obj.title for obj in shift_app_plans]
        shift_app_plan_prices = [obj.price for obj in shift_app_plans]
        context = {
            'form': form,
            'shift_app_plan_titles': shift_app_plan_titles,
            'shift_app_plan_prices': shift_app_plan_prices,
        }
        if not form.is_valid():
            return render(request, 'shiftApp/registration.html', context)

        shift_app = form.save(commit=False)
        shift_app.user = request.user
        shift_app.save()
        return redirect('shiftApp:home')


class ShiftAppUpdateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """勤務表作成機能更新画面"""
    template_name = 'shiftApp/update.html'

    def get(self, request, *args, **kwargs):
        shift_app = get_object_or_404(ShiftApp, pk=request.user.id)
        shift_app_plans = ShiftAppPlan.objects.all()
        shift_app_plan_titles = [obj.title for obj in shift_app_plans]
        shift_app_plan_prices = [obj.price for obj in shift_app_plans]
        context = {
            'form': ShiftAppRegistrationForm(None, instance=shift_app),
            'shift_app': shift_app,
            'shift_app_plan_titles': shift_app_plan_titles,
            'shift_app_plan_prices': shift_app_plan_prices,
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        shift_app = get_object_or_404(ShiftApp, pk=request.user.id)
        shift_app_plan = get_object_or_404(ShiftAppPlan, pk=request.POST['plan'])
        shift_app.plan = shift_app_plan
        form = ShiftAppRegistrationForm(request.POST, instance=shift_app)
        if not form.is_valid():
            shift_app_plans = ShiftAppPlan.objects.all()
            shift_app_plan_titles = [obj.title for obj in shift_app_plans]
            shift_app_plan_prices = [obj.price for obj in shift_app_plans]
            context = {
                'form': form,
                'shift_app_plan_titles': shift_app_plan_titles,
                'shift_app_plan_prices': shift_app_plan_prices,
            }
            return render(request, 'shiftApp/update.html', context)

        form.save()

        return redirect('shiftApp:setting')

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk']


class ShiftAppCancellationView(LoginRequiredMixin, DeleteView):
    """勤務表作成機能解約画面"""

    def get(self, request, *args, **kwargs):
        shift_app = get_object_or_404(ShiftApp, pk=request.user.id)
        context = {
            'shift_app': shift_app,
        }
        return render(request, 'shiftApp/cancellation.html', context)


class ShiftAppSettingView(LoginRequiredMixin, TemplateView):
    """勤務表設定画面"""
    template_name = 'shiftApp/setting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shift_app = get_object_or_404(ShiftApp, pk=self.request.user.id)
        context['shift_app'] = shift_app
        return context


class ShiftAppHomeView(LoginRequiredMixin, View):
    """勤務表作成機能ホーム画面"""

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'shiftApp/home.html', context)
