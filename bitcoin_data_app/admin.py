# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from bitcoin_data_app.models import Transaction_Table, Input_Table, Output_Table, Block_Table

#admin.site.register(Block_Header_Table)
admin.site.register(Transaction_Table)
admin.site.register(Output_Table)
admin.site.register(Input_Table)
admin.site.register(Block_Table)


# Register your models here.
