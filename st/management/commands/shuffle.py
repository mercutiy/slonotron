from django.core.management import BaseCommand

from st.models import Party, Member, Score
from st.utils import shuffle


class Command(BaseCommand):
    help = 'Shuffle the members of the pary'

    def add_arguments(self, parser):
        parser.add_argument('party_id', type=int)
        parser.add_argument('-dr', '--dry_run', action='store_true', help="Dry run")

    def handle(self, party_id, dry_run, **kwargs):
        try:
            party = Party.objects.get(id=party_id)
        except Party.DoesNotExist:
            self.stdout.write('Cannot find the party {}'.format(party_id))
            return
        if party.status != Party.ACTIVE:
            self.stdout.write('Wrong party status. Check it with admin.')
            return
        try:
            best_path = shuffle(party, dry_run)
        except Exception as e:
            self.stdout.write('Exception happened')
            return
        members = dict(
            Member.objects.filter(party=party).values_list('id', 'user__username'))
        members_count = len(best_path)
        for i in range(members_count):
            from_member = best_path[i]
            to_member = best_path[(i + 1) % members_count]
            try:
                score = Score.objects.get(
                    from_member=best_path[i],
                    to_member=best_path[(i + 1) % members_count]
                ).value
            except Score.DoesNotExist:
                score = 5
            self.stdout.write(
                '{} -{}-> {}'.format(members[from_member], score, members[to_member]))
        self.stdout.write('Members have been shuffled!')
