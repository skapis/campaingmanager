from django.urls import path
from .views import SendAllInCampaign, CheckEmailLimit, TemplateDashboard, TemplateDetail
from . import views

urlpatterns = [
    path('campaign/<uuid:id>', SendAllInCampaign.as_view(), name='all_in_campaign'),
    path('check-limit', CheckEmailLimit.as_view(), name='check_limit'),
    path('templates', TemplateDashboard.as_view(), name='templates'),
    path('template/<uuid:id>', TemplateDetail.as_view(), name='template'),
    path('template/<uuid:id>/delete', views.delete_template, name='delete_template')
]