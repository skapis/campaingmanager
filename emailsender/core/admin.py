from django.contrib import admin
from .models import Customer, Campaign, CampaignToCustomer, Gender


admin.site.register(Customer)
admin.site.register(Campaign)
admin.site.register(CampaignToCustomer)
admin.site.register(Gender)



