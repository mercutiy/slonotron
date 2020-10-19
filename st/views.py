from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from st.forms import ScalesForm
from st.models import Party, Member, Score


def login(request):
    return render(request, 'login.html')


@login_required
def parties(request):
    party_list = Party.objects.get_user_parties(request.user, Party.ACTIVE)
    context = {'parties': party_list}
    return render(request, 'parties.html', context)


@login_required
def party(request, party_id):
    try:
        party_obj = Party.objects.get(id=party_id)
    except Party.DoesNotExist:
        return redirect('parties')
    curr_member = Member.objects.get(party=party_obj, user=request.user)
    members = Member.objects.filter(party=party_obj).exclude(id=curr_member.id)
    scores = dict(
        Score.objects.filter(from_member=curr_member).values_list('to_member__id', 'value'))
    for member in members:
        member.score = scores.get(member.id, 5)

    if request.method == 'POST':
        form = ScalesForm(curr_member, members, request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            updated_scores = [
                Score(
                    from_member_id=curr_member.id,
                    to_member_id=int(member_key[6:]),
                    value=value
                ) for member_key, value in form.cleaned_data.items() if value != 5
            ]
            Score.objects.filter(from_member=curr_member).delete()
            Score.objects.bulk_create(updated_scores)
            return redirect('party', party_id=party_id)
    else:
        form = ScalesForm(curr_member, members)

    context = {
        'party': party_obj,
        'curr_member': curr_member,
        'members': members,
        'form': form
    }
    return render(request, 'party.html', context)


@login_required
def user(request, user_id):
    return render(request, 'base.html')
