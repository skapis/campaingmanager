import json
import threading
from datetime import datetime as dt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from core.models import Campaign, Customer, CampaignToCustomer
from django.views import View
from django.core.mail import EmailMultiAlternatives
from .models import EmailLog, EmailLimit, EmailTemplate
from django.contrib import messages
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class SendAllInCampaign(View):
    def post(self, request, id):
        campaign = Campaign.objects.get(campaignId=id)
        email_limit = EmailLimit.objects.get(name='Email')
        if campaign.active:
            c2c = CampaignToCustomer.objects.filter(campaign=campaign)
            if c2c.count() != 0:
                if c2c.count() <= email_limit.limit:
                    from_email = 'noreply@campaignmanager.com'
                    subject = campaign.template.subject
                    plaintext = get_template(f'email_templates/{campaign.template.file_name}.txt')
                    htmly = get_template(f'email_templates/{campaign.template.file_name}.html')
                    for cust in c2c:
                        d = {
                            'customer': cust.customer,
                            'content': campaign.template
                        }
                        to_mail = cust.customer.email
                        text_content = plaintext.render(d)
                        html_content = htmly.render(d)
                        email_msg = EmailMultiAlternatives(subject, text_content, from_email, [to_mail])
                        email_msg.attach_alternative(html_content, 'text/html')
                        EmailThread(email_msg).start()
                        EmailLog.objects.create(campaignId=campaign.campaignId, campaign=campaign.name,
                                                customerId=cust.customer.customerId, customer=cust.customer.email)
                        email_limit.limit = email_limit.limit - 1
                        email_limit.save()
                    messages.success(request, 'Emails were succesfully sent')
                    return redirect('campaign', id)
                else:
                    messages.error(request, 'Your email limit is too low to send emails to all customers')
                    return redirect('campaign', id)
            messages.error(request, 'The campaign does not have any customers')
            return redirect('campaign', id)
        messages.error(request, 'The campaign is not active')
        return redirect('campaign', id)


class CheckEmailLimit(View):
    def get(self, request):
        email_limit = EmailLimit.objects.get(name='Email')
        if email_limit.resetDate != dt.now().date():
            email_limit.limit = 500
            email_limit.resetDate = dt.now().date()
            email_limit.save()
            return JsonResponse({'message': 'Limit reset'}, status=200, safe=False)
        return JsonResponse({'message': f'Reset date is {email_limit.resetDate}'})


class TemplateDashboard(View):
    def get(self, request):
        templates = EmailTemplate.objects.all()
        campaigns = Campaign.objects.all()
        p = Paginator(templates, 5)
        page_number = request.GET.get('page', None)
        page_obj = Paginator.get_page(p, page_number)
        context = {
            'page_obj': page_obj,
            'campaigns': campaigns
        }
        return render(request, 'emails/index.html', context)

    def post(self, request):
        name = request.POST['name']
        subject = request.POST['subject']
        content = request.POST['content']
        header = request.POST['header']

        if not name or not subject or not content or not header:
            messages.error(request, 'You must fill all required fields')
            return redirect('templates')

        if EmailTemplate.objects.filter(name=name).exists():
            messages.error(request, 'Template with this name is already exist, please choose another one')
            return redirect('templates')

        EmailTemplate.objects.create(name=name, subject=subject, content=content, header=header, file_name='default')

        messages.success(request, 'Template was succesfully created')
        return redirect('templates')


class TemplateDetail(View):
    def get(self, request, id):
        template = EmailTemplate.objects.get(templateId=id)
        context = {
            'template': template
        }

        return render(request, 'emails/detail.html', context)

    def post(self, request, id):
        data = json.loads(request.body)
        name = data['name']
        subject = data['subject']
        content = data['content']
        header = data['header']

        if not name or not subject or not content or not header:
            return JsonResponse({'message': 'All required fields must be filled'}, status=400)

        template = EmailTemplate.objects.get(templateId=id)
        template.name = name
        template.subject = subject
        template.header = header
        template.content = content
        template.save()

        resp = {
            'name': name,
            'subject': subject,
            'header': header,
            'content': content
        }
        return JsonResponse(resp, status=200)


def delete_template(request, id):
    template = EmailTemplate.objects.get(templateId=id)
    template.delete()
    messages.success(request, f'Template {template.name} was removed')
    return redirect('templates')


