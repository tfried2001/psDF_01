from django.contrib import admin

# Register your models here.

from .models import Invitation

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'message', 'timestamp',)
    list_editable = ('from_user', 'to_user',)
