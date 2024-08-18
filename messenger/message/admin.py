from django.contrib import admin

from message.models import Messages


@admin.register(Messages)
class AdminMessages(admin.ModelAdmin):
    list_display = (
        Messages.author.field.name,
        Messages.content.field.name,
        Messages.created_at.field.name,
    )


__all__ = []