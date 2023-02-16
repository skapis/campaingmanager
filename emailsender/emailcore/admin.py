from django.contrib import admin
from .models import EmailLog, EmailLimit, EmailTemplate

admin.site.register(EmailLog)
admin.site.register(EmailLimit)
admin.site.register(EmailTemplate)
