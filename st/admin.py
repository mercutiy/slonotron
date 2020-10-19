from django import forms
from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf.urls import url
from django.urls import path
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError, HttpResponse

from st.utils import shuffle
from .models import Party, Member, Score


class MemberInlineForm(forms.ModelForm):
    stop_list = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Member
        fields = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            other_members = self.instance.party.member_set.exclude(member=self.instance)
            self.fields['user'].disabled = True
            self.fields['stop_list'].choices = ((om.id, om.user.username) for om in other_members)
            self.fields['stop_list'].initial = list(
                Score.objects.filter(
                    from_member=self.instance, value=0).values_list('to_member', flat=True))

            # users = User.objects.filter(
            #     member__party=self.instance.party).exclude(member=self.instance)
            # self.fields['user'].disabled = True
            #
            # self.fields['stop_list'].choices = ((u.id, u.username) for u in users)
            # self.fields['stop_list'].initial = list(
            #     Score.objects.filter(
            #         from_member=self.instance, value=0).values_list('to_member', flat=True))


    def save(self, commit=True):
        res = super().save(commit)
        self._save_stop_list()
        return res

    def _save_stop_list(self):
        stop_list = self.cleaned_data.get('stop_list', [])
        scores = [
            Score(
                from_member=self.instance,
                to_member_id=int(tm_id),
                value=0
            ) for tm_id in stop_list
        ]
        Score.objects.filter(
            Q(value=0) | Q(to_member_id__in=stop_list),
            from_member=self.instance
        ).delete()
        Score.objects.bulk_create(scores)


class MemberInline(admin.TabularInline):
    model = Member
    form = MemberInlineForm



class PartyAdmin(admin.ModelAdmin):
    inlines = (MemberInline,)
    list_display = ('name', 'date', 'status')
    change_form_template = 'admin/party_change_form.html'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=Party.INACTIVE)

    def get_urls(self):
        custom_urls = [path(
            '<path:party_id>/activate/',
            self.admin_site.admin_view(self.activate_party),
            name='st_party_activate'
        )]
        return custom_urls + super().get_urls()

    def activate_party(self, request, party_id):
        try:
            party = Party.objects.get(id=party_id, status=Party.INACTIVE)
        except Party.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Cannot find the party or it is already activated')
            return HttpResponseNotFound()
        if not shuffle(party, check=True):
            messages.add_message(request, messages.ERROR, 'Cannot shuffle members. Probably the rules are too strict.')
            return HttpResponseServerError()
        party.status = Party.ACTIVE
        party.save()
        messages.add_message(request, messages.INFO, 'The party have been activated')
        # todo: use json response
        return HttpResponse()





admin.site.register(Party, PartyAdmin)
