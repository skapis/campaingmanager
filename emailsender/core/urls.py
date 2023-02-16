from django.urls import path
from . import views
from .views import EmailValidation, RemoveCustFromCamp, AddCustToCamp, AddCampToCust, AvailableCampList,\
    ToggleCampaignState, AvailableCustList, CampaignDetail, CustomerDetail, Customers, Campaigns, CustomersBulkInsert,\
    CampaignsBulkInsert, Dashboard


urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('campaigns', Campaigns.as_view(), name='campaigns'),
    path('campaigns/bulk', CampaignsBulkInsert.as_view(), name='campaigns_bulk'),
    path('check-email', EmailValidation.as_view(), name='check_mail'),
    path('customers', Customers.as_view(), name='customers'),
    path('customers/bulk', CustomersBulkInsert.as_view(), name='customers_bulk'),
    path('customer/<uuid:id>', CustomerDetail.as_view(), name='customer'),
    path('customer/<uuid:id>/add-camp', AddCampToCust.as_view(), name='customer_add_camp'),
    path('campaign/<uuid:id>/add-custs', AddCustToCamp.as_view(), name='campaign_add_cust'),
    path('customer/<uuid:id>/delete', views.delete_customer, name='delete_customer'),
    path('campaign/<uuid:id>', CampaignDetail.as_view(), name='campaign'),
    path('campaign/<uuid:id>/delete', views.delete_campaign, name='delete_campaign'),
    path('remove-camp-cust', RemoveCustFromCamp.as_view(), name='remove_c2c'),
    path('customer/available-camps', AvailableCampList.as_view(), name='cust_available_camps'),
    path('campaign/available-custs', AvailableCustList.as_view(), name='camp_available_custs'),
    path('campaign/change-state', ToggleCampaignState.as_view(), name='toggle_campaign_state')
]
