#coding=utf-8

from django.dispatch import Signal

timeline_added = Signal(providing_args=[])
notification_added = Signal(providing_args=[])

follower_added = Signal(providing_args=["followee"])
follower_deleted = Signal(providing_args=["followee"])