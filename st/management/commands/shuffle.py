from datetime import datetime

from django.core.management import BaseCommand
from django.db.models import Q

from st.models import Party, Member, Score
from st.utils import shuffle


class Command(BaseCommand):
    help = 'Shuffle the members of the pary'

    def add_arguments(self, parser):
        parser.add_argument('party_id', type=int)
        parser.add_argument('-dr', '--dry_run', action='store_true', help="Dry run")
        parser.add_argument('-c', '--check', action='store_true', help="Check possibility")

    def handle(self, party_id: int, dry_run: bool, check: bool, **kwargs) -> None:
        if party_id:
            try:
                party = Party.objects.get(id=party_id)
            except Party.DoesNotExist:
                self.stdout.write('Cannot find the party {}'.format(party_id))
                return
            self.shuffle_party(party, dry_run, check)
        else:
            parties = Party.objects.filter(
                Q(start_game__lt=datetime.now()) | ~Q(member__is_applied=False),
                status=Party.ACTIVE
            )
            if not parties:
                self.stdout.write('No active parties found')
                return
            for party in parties:
                self.shuffle_party(party, dry_run, check)

    def shuffle_party(self, party: Party, dry_run: bool, check: bool) -> None:
        self.stdout.write('Shuffling party {}'.format(party.id))
        if party.status != Party.ACTIVE:
            self.stdout.write('Wrong party status')
            return
        best_path = shuffle(party, dry_run, check)
        if not best_path:
            self.stdout.write('Impossible to shuffle')
            return
        members = dict(
            Member.objects.filter(party=party).values_list('id', 'user__username'))
        members_count = len(best_path)
        total_score = 0
        for i in range(members_count):
            from_member = best_path[i]
            to_member = best_path[(i + 1) % members_count]
            try:
                score = Score.objects.get(from_member=from_member, to_member=to_member).value
            except Score.DoesNotExist:
                score = 5
            total_score += score
            self.stdout.write(
                '{} -{}-> {}'.format(members[from_member], score, members[to_member]))
        self.stdout.write('Members have been shuffled! Total score: {}'.format(total_score))
