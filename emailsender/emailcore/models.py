import uuid
from django.db import models
from django.utils.timezone import now


class EmailLog(models.Model):
    campaignId = models.UUIDField()
    campaign = models.CharField(max_length=255)
    customerId = models.UUIDField()
    customer = models.EmailField()
    templateId = models.UUIDField(null=True)
    template = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.campaign} - {self.customer}"

    class Meta:
        verbose_name_plural = 'EmailLog'
        ordering = ['-timestamp']


class EmailLimit(models.Model):
    name = models.CharField(max_length=255)
    limit = models.IntegerField(null=True)
    resetDate = models.DateField(default=now)

    def __str__(self):
        return self.name


class EmailTemplate(models.Model):
    templateId = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    header = models.CharField(max_length=255)
    content = models.TextField()
    file_name = models.CharField(max_length=255, default='default')
    created = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']

