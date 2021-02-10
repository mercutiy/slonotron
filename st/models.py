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
    date = models.DateField(null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=INACTIVE)
    start_game = models.DateTimeField(null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

    class Meta:
        verbose_name_plural = 'parties'

    def __str__(self):
        return self.name

    class Manager(models.Manager):
        def get_user_parties(self, user, statuses=None):
            parties = self.filter(member__user=user)
            if statuses:
                parties = parties.filter(status__in=statuses)
            return parties.order_by('-date')

    objects = Manager()


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    present_to = models.OneToOneField('Member', on_delete=models.CASCADE,
                                      null=True, default=None)
    is_applied = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'party')

    def __str__(self):
        return '{} at {}'.format(self.user.username, self.party.name)


class Score(models.Model):
    from_member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='from_score')
    to_member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='to_score')
    value = models.SmallIntegerField(default=5)
