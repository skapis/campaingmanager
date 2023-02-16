import uuid
from django.db import models
from django.utils.timezone import now
from emailcore.models import EmailTemplate


class Gender(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Customer(models.Model):
    customerId = models.UUIDField(default=uuid.uuid4)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.ForeignKey(to=Gender, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    age = models.IntegerField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['email']


class Campaign(models.Model):
    campaignId = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    template = models.ForeignKey(to=EmailTemplate, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']


class CampaignToCustomer(models.Model):
    c2cId = models.UUIDField(default=uuid.uuid4)
    campaign = models.ForeignKey(to=Campaign, on_delete=models.CASCADE)
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.campaign.name} - {self.customer.email}"

    class Meta:
        verbose_name_plural = 'Campaigns2Customers'


