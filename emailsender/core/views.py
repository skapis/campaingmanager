from django.shortcuts import render, redirect
from .models import Customer, Campaign, CampaignToCustomer, Gender
from django.contrib import messages
from django.http import JsonResponse
import json
from django.views import View
from validate_email import validate_email
from emailcore.models import EmailLog, EmailLimit, EmailTemplate
from django.core.paginator import Paginator


class Dashboard(View):
    def get(self, request):
        customers = Customer.objects.all()
        campaigns = Campaign.objects.all()
        email_limit = EmailLimit.objects.get(name='Email')
        camp_list = []
        for campaign in campaigns:
            camp = {
                'id': campaign.campaignId,
                'name': campaign.name,
                'description': campaign.description,
                'active': campaign.active,
                'custs': CampaignToCustomer.objects.filter(campaign=campaign).count()
            }
            camp_list.append(camp)

        context = {
            'custs': customers.count(),
            'camps': campaigns.count(),
            'limit': email_limit.limit,
            'camp_list': camp_list
        }

        if email_limit.limit == 0:
            messages.error(request,
                           f"You have reached email limit, until {email_limit.resetDate} you can't send emails")
        return render(request, 'dashboard.html', context)


class Campaigns(View):
    def get(self, request):
        campaigns = Campaign.objects.all()
        p = Paginator(campaigns, 5)
        page_number = request.GET.get('page', None)
        page_obj = Paginator.get_page(p, page_number)
        email_limit = EmailLimit.objects.get(name='Email')
        templates = EmailTemplate.objects.all()
        context = {
            'page_obj': page_obj,
            'limit': email_limit.limit,
            'templates': templates
        }

        if email_limit.limit == 0:
            messages.error(request,
                           f"You have reached email limit, until {email_limit.resetDate} you can't send emails")
        return render(request, 'campaigns/index.html', context)

    def post(self, request):
        name = request.POST['name']
        description = request.POST['description']
        template = request.POST['template']
        active_list = request.POST.getlist('active')
        if len(active_list) != 0:
            active = True
        else:
            active = False

        if name and description:
            email_template = EmailTemplate.objects.get(templateId=template)
            Campaign.objects.create(name=name, description=description, template=email_template, active=active)
            messages.success(request, f'Campaign {name} was successfully created')
            return redirect('campaigns')

        messages.error(request, 'All fields are required')
        return redirect('campaigns')


class Customers(View):
    def get(self, request):
        customers = Customer.objects.all()
        p = Paginator(customers, 5)
        page_number = request.GET.get('page', None)
        page_obj = Paginator.get_page(p, page_number)
        genders = Gender.objects.all()
        context = {
            'page_obj': page_obj,
            'genders': genders
        }
        return render(request, 'customers/index.html', context)

    def post(self, request):
        email = request.POST['email']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        age = request.POST['age']
        gender = request.POST['gender']
        birthdate = request.POST['birthDate']

        if email and first_name and last_name and age and gender and birthdate:
            Customer.objects.create(email=email.lower(), first_name=first_name, last_name=last_name,
                                    age=age, gender=Gender.objects.get(pk=gender), birthdate=birthdate)
            messages.success(request, f'Customer {email} was succesfully created')
            return redirect('customers')

        messages.error(request, 'All fields are required')
        return redirect('customers')


class CustomerDetail(View):
    def get(self, request, id):
        customer = Customer.objects.get(customerId=id)
        genders = Gender.objects.all()
        campaigns = CampaignToCustomer.objects.filter(customer=customer.pk)
        emails = EmailLog.objects.filter(customerId=id)
        context = {
            'customer': customer,
            'c2cs': campaigns,
            'emails': emails,
            'genders': genders
        }
        return render(request, 'customers/detail.html', context)

    def post(self, request, id):
        customer = Customer.objects.get(customerId=id)
        data = json.loads(request.body)
        email = data['email']
        first_name = data['firstName']
        last_name = data['lastName']
        age = data['age']
        gender = data['gender']
        birthdate = data['birthDate']

        if email and first_name and last_name and age and gender and birthdate:
            customer.email = email
            customer.first_name = first_name
            customer.last_name = last_name
            customer.age = age
            customer.gender = Gender.objects.get(pk=gender)
            customer.birthdate = birthdate
            customer.save()

            response = {
                'email': email,
                'firstName': first_name,
                'lastName': last_name,
                'age': age,
                'gender': gender,
                'birthDate': birthdate
            }

            return JsonResponse(response, status=200)
        return JsonResponse({'message': 'Something is wrong, check data and try again'}, status=400)


def delete_customer(request, id):
    customer = Customer.objects.get(customerId=id)
    customer.delete()

    messages.success(request, f'Customer {customer.email} was succesfully deleted')
    return redirect('customers')


class AvailableCampList(View):
    def get(self, request):
        cust_id = request.GET.get('custId', None)
        if cust_id:
            cust = Customer.objects.get(customerId=cust_id)
            c2c = CampaignToCustomer.objects.filter(customer=cust)
            camps = Campaign.objects.exclude(pk__in=c2c.values_list('campaign'))
            return JsonResponse(list(camps.values()), safe=False)
        return JsonResponse({'error': 'custId is required'})


class CampaignDetail(View):
    def get(self, request, id):
        campaign = Campaign.objects.get(campaignId=id)
        c2c = CampaignToCustomer.objects.filter(campaign=campaign)
        emails = EmailLog.objects.filter(campaignId=id)
        email_limit = EmailLimit.objects.get(name='Email')
        templates = EmailTemplate.objects.all()
        context = {
            'campaign': campaign,
            'c2cs': c2c,
            'emails': emails,
            'limit': email_limit.limit,
            'templates': templates
        }
        if not campaign.active:
            messages.error(request, 'This campaign is not enabled, you cannot send emails, until you enable it.')

        if email_limit.limit == 0:
            messages.error(request,
                           f"You have reached email limit, until {email_limit.resetDate} you can't send emails")
        return render(request, 'campaigns/detail.html', context)

    def post(self, request, id):
        campaign = Campaign.objects.get(campaignId=id)
        data = json.loads(request.body)
        name = data['name']
        description = data['description']
        template = data['template']

        if name and description:
            campaign.name = name
            campaign.description = description
            campaign.template = EmailTemplate.objects.get(templateId=template)
            campaign.save()
            response = {
                'name': campaign.name,
                'description': campaign.description,
                'template': campaign.template.templateId
            }
            return JsonResponse(response, safe=False, status=200)
        return JsonResponse({'err': 'Name, Description and Template are required'}, status=400)


def delete_campaign(request, id):
    campaign = Campaign.objects.get(campaignId=id)
    campaign.delete()

    messages.success(request, f'Campaign {campaign.name} was removed')
    return redirect('campaigns')


class AvailableCustList(View):
    def get(self, request):
        camp_id = request.GET.get('campId', None)
        if camp_id:
            camp = Campaign.objects.get(campaignId=camp_id)
            c2c = CampaignToCustomer.objects.filter(campaign=camp)
            custs = Customer.objects.exclude(pk__in=c2c.values_list('customer'))
            return JsonResponse(list(custs.values()), safe=False)
        return JsonResponse({'error': 'campId is required'})


# View for add campaigns to one customer
class AddCampToCust(View):
    def post(self, request, id):
        camps = request.POST.getlist('camps')
        cust = Customer.objects.get(customerId=id)
        for camp in camps:
            campaign = Campaign.objects.get(campaignId=camp)
            if not CampaignToCustomer.objects.filter(campaign=campaign, customer=cust).exists():
                CampaignToCustomer.objects.create(campaign=campaign, customer=cust)
                messages.success(request, f'Customer was added to {campaign.name}')
        return redirect('customer', cust.customerId)


# View for add customers to one campaign
class AddCustToCamp(View):
    def post(self, request, id):
        custs = request.POST.getlist('custs')
        campaign = Campaign.objects.get(campaignId=id)
        for cust in custs:
            customer = Customer.objects.get(customerId=cust)
            if not CampaignToCustomer.objects.filter(campaign=campaign, customer=customer).exists():
                CampaignToCustomer.objects.create(campaign=campaign, customer=customer)
                messages.success(request, f'{customer.email} was added to {campaign.name}')
        return redirect('campaign', campaign.campaignId)


class RemoveCustFromCamp(View):
    def post(self, request):
        data = json.loads(request.body)
        c2c = CampaignToCustomer.objects.get(c2cId=data['ccId'])
        c2c.delete()
        response = {
            'message': f'{c2c.customer.email} was removed from campaign {c2c.campaign.name}',
            'id': c2c.c2cId
        }
        return JsonResponse(response, status=200)


class ToggleCampaignState(View):
    def post(self, request):
        data = json.loads(request.body)
        camp_id = data['campId']
        if camp_id:
            campaign = Campaign.objects.get(campaignId=camp_id)
            campaign.active = not campaign.active
            campaign.save()
            return JsonResponse({'state': campaign.active}, status=200)
        return JsonResponse({'err': 'Campaign ID is required'}, status=400)


class CustomersBulkInsert(View):
    def post(self, request):
        data = json.loads(request.body)
        custs = data['customers']
        errs = []
        cust_list = []
        for cust in custs:
            first_name = cust['firstName']
            last_name = cust['lastName']
            email = cust['email']
            gender = cust['gender']
            age = cust['age']
            birthdate = cust['birthdate']
            try:
                campaign = cust['campaign']
            except:
                campaign = ''

            try:
                if not Customer.objects.filter(email=email).exists():
                    customer = Customer.objects.create(first_name=first_name, last_name=last_name, email=email,
                                                       gender=Gender.objects.get(name=gender), age=age,
                                                       birthdate=birthdate)
                    if Campaign.objects.filter(name=campaign).exists():
                        camp = Campaign.objects.get(name=campaign)
                        CampaignToCustomer.objects.create(campaign=camp, customer=customer)
                    cust_json = {
                        'custId': customer.customerId,
                        'name': f'{customer.first_name} {customer.last_name}',
                        'email': customer.email,
                        'gender': gender,
                        'age': customer.age,
                        'birthdate': customer.birthdate
                    }
                    cust_list.append(cust_json)
            except:
                errs.append(email)

        resp = {
            'created': len(custs) - len(errs),
            'customers': cust_list,
            'errs': errs
        }
        return JsonResponse(resp, status=200)


class CampaignsBulkInsert(View):
    def post(self, request):
        data = json.loads(request.body)
        camps = data['campaigns']
        errs = []
        camp_list = []
        for camp in camps:
            name = camp['name']
            description = camp['description']
            template = camp['template']

            try:
                if not Campaign.objects.filter(name=name).exists():
                    if EmailTemplate.objects.filter(name=template).exists():
                        campaign = Campaign.objects.create(name=name, description=description,
                                                           template=EmailTemplate.objects.get(name=template))
                    else:
                        campaign = Campaign.objects.create(name=name, description=description,
                                                           template=EmailTemplate.objects.get(name='Default'))

                    camp_json = {
                        'campId': campaign.campaignId,
                        'name': campaign.name,
                        'description': campaign.description,
                        'template': campaign.template.name
                    }
                    camp_list.append(camp_json)
            except:
                errs.append(name)

        resp = {
            'created': len(camps) - len(errs),
            'campaigns': camp_list,
            'errs': errs
        }
        return JsonResponse(resp, status=200)


class EmailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'emailError': 'Email is invalid'}, status=400)
        if Customer.objects.filter(email=email).exists():
            return JsonResponse({'emailError': 'E-mail is already taken'}, status=409)
        return JsonResponse({'emailValid': True})

