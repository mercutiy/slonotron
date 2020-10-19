from django.contrib.auth.models import User
from django.db import models


class Party(models.Model):
    INACTIVE = 0
    ACTIVE = 1
    PLAYED = 2
    STATUS_CHOICES = (
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
        (PLAYED, 'Played'),
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date = models.DateField()
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=INACTIVE)
    start_game = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'parties'

    def __str__(self):
        return self.name

    class Manager(models.Manager):
        def get_user_parties(self, user, status=None):
            parties = self.filter(member__user=user)
            if status:
                parties = parties.filter(status=status)
            return parties

    objects = Manager()


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.PROTECT)
    present_to = models.OneToOneField('Member', on_delete=models.PROTECT,
                                      null=True, default=None)

    class Meta:
        unique_together = ('user', 'party')

    def __str__(self):
        return '{} at {}'.format(self.user.username, self.party.name)


class Score(models.Model):
    from_member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='from_scale')
    to_member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='to_scale')
    value = models.SmallIntegerField(default=5)
