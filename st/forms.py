from django import forms
from django.forms import Widget, NumberInput


class Slider(NumberInput):
    class Media:
        js = ('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/11.0.2/bootstrap-slider.min.js',)
        css = {'screen': ('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/11.0.2/css/bootstrap-slider.min.css',), }


class ScalesForm(forms.Form):
    class Media:
        js = ('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/11.0.2/bootstrap-slider.min.js',)
        css = {'screen': ('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/11.0.2/css/bootstrap-slider.min.css',), }

    def __init__(self, curr_member, members, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.curr_member = curr_member
        for member in members:
            attrs = {
                'class': 'slider',
                'data-slider-min': 1,
                'data-slider-max': 10,
                'data-slider-step': 1,
                'data-slider-value': member.score
            }
            self.fields['value_{}'.format(member.id)] = forms.IntegerField(
                label=member.user.username, min_value=1, max_value=10,
                initial=member.score, widget=Slider(attrs=attrs))
