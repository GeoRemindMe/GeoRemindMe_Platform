# coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
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
            if not User.objects.filter(username=r[1]).exists():
                User(email=r[0],
                     username=r[1],
                     password=r[2],
                     date_joined=r[3]).save()
        return sys.exit(0)