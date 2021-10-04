from django.contrib import admin

from .forms import ProfileForn
from .models import Message
from .models import Profile

@admin.register(Profile)
class profileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForn

@admin.register(Message)
class profileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at')

    # def get_queryset(self, request):
    #     return