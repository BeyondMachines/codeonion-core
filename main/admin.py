from django.contrib import admin

from main.models import Message

# Register your models here.

class MessageModelAdmin(admin.ModelAdmin):
    list_display = ('message_title', 'message_created_date')

    def get_topic(self, obj):  # using this we can render the foreign key information
        return obj.message_title

admin.site.register(Message, MessageModelAdmin)
