from django import forms

from .models import ShiftApp, ShiftAppPlan


class ShiftAppRegistrationForm(forms.ModelForm):
    """勤務表作成機能登録用フォーム"""

    plan = forms.ModelChoiceField(
        queryset=ShiftAppPlan.objects.all(),
        empty_label=None,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].widget.attrs['class'] = 'plan-radio form-check-input'

    class Meta:
        model = ShiftApp
        fields = ('plan',)
