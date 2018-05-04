from django.contrib import admin

from .models import Board
from .models import Topic

admin.site.register(Board)
admin.site.register(Topic)