# coding=utf-8

import watchers

from django.contrib import auth


def natural_key(self):
    return (self.pk, self.username)

auth.models.User.add_to_class('natural_key', natural_key)


