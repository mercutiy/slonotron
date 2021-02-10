from django import forms
from django.forms import NumberInput
from django.contrib.auth.models import User

from st.models import Party


class Slider(NumberInput):
    class Media:
        js = ('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/11.0.2/bootstrap-slider.min.js',)
        css = {'screen': ('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/11.0.2/css/bootstrap-slider.min.css',), }

    def __init__(self, score):
        self.min_value = 1
        self.max_value = 10
        super().__init__(
            {
                'class': 'slider',
                'data-slider-min': self.min_value,
                'data-slider-max': self.max_value,
                'data-slider-step': 1,
                'data-slider-value': score
            }
        )


class ScalesForm(forms.Form):
    def __init__(self, curr_member, members, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.curr_member = curr_member
        for member in members:
            widget = Slider(member.score)
            self.fields['value_{}'.format(member.id)] = forms.IntegerField(
                label=member.user.username,
                min_value=widget.min_value,
                max_value=widget.max_value,
                initial=member.score,
                widget=widget
            )


class PartyForm(forms.ModelForm):

    class Meta:
        model = Party
        fields = ['name', 'description', 'date']

    def __init__(self, admin: User, *args, **kwargs):
        self.admin = admin
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.admin = self.admin
        if commit:
            super().save()
        return instance

