# coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from apps.timelines.models import Follower
import csv
import sys


class Command(BaseCommand):
    args = '.csv'
    
    def handle(self, *args, **options):
        file = csv.reader(open(args[0], 'r'), delimiter='#')
        rownum = 0
        for r in file:
            if rownum == 0:
                rownum=rownum+1
                continue
            try:
                follower = User.objects.get(username=r[0])
                followee = User.objects.get(username=r[1])
                if not Follower.objects.is_follower(follower, followee):
                    Follower.objects.toggle_follower(follower, followee)
            except User.DoesNotExist:
                pass
        return sys.exit(0)