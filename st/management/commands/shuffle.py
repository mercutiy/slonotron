from django.core.management import BaseCommand

from st.models import Party
from st.utils import shuffle


class Command(BaseCommand):
    help = 'Shuffle the members of the pary'

    def add_arguments(self, parser):
        parser.add_argument('--party_id', type=int)

    def handle(self, party_id, **kwargs):
        try:
            party = Party.objects.get(id=party_id)
        except Party.DoesNotExist:
            self.stdout.write('Cannot find the party {}'.format(party_id))
            return
        if party.status != Party.ACTIVE:
            self.stdout.write('Wrong party status. Check it with admin.')
            return
        try:
            shuffle(party)
        except Exception as e:
            print('asdfasfasf!!!')
            self.stdout.write('Exception happened')
            print(e)
            return
        self.stdout.write('Members have been shuffled!')
