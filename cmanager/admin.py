# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from cmanager.models import *

admin.site.register(User, UserAdmin)
admin.site.register(Game)
admin.site.register(GiftCode)
admin.site.register(GiftCodeToUser)
admin.site.register(Lottery)
admin.site.register(Promotions)