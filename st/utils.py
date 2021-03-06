import itertools
import random
from collections import defaultdict

from .models import Score, Member, Party


def shuffle(party, dry_run=False, check=False):
    members = party.member_set.all()
    scores = Score.objects.filter(from_member__in=members).values_list(
        'from_member_id', 'to_member_id', 'value')
    matrix = defaultdict(dict)
    for from_member_id, to_member_id, value in scores:
        matrix[from_member_id][to_member_id] = value

    for from_member in members:
        for to_member in members:
            if from_member == to_member:
                matrix[from_member.id][to_member.id] = 0
            else:
                matrix[from_member.id].setdefault(to_member.id, 5)

    best_path = calc_best_path(matrix, any_path=check)

    if dry_run or check:
        return best_path
    if not best_path:
        return None

    for i in range(len(members)):
        Member.objects.filter(id=best_path[i]).update(present_to_id=best_path[(i + 1) % len(members)])
    party.status = Party.PLAYED
    party.save()
    return best_path


def calc_best_path(matrix, any_path=False):
    members_list = list(matrix.keys())
    random.shuffle(members_list)
    members = len(members_list)
    best_path = []
    best_score = 0
    for curr_path in itertools.permutations(members_list):
        curr_score = 0
        for i in range(members):
            score = matrix[curr_path[i]][curr_path[(i + 1) % members]]
            if score == 0:
                curr_score = 0
                break
            curr_score += score
        if best_score < curr_score:
            if any_path:
                return curr_path
            best_score = curr_score
            best_path = curr_path
    return best_path or None


