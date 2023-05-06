# Campaing Manager
In this repository is a simple app for managing campaigns and customers. This app is developed in Django Framework and it uses also JQuery. This app is based on three main instances, customers, campaigns and email templates. Users can create, edit or delete customers and add them to campaigns and then send them emails. Each customer can be added to one or more campaigns. Each campaign can have one current email template. Users can create, edit or delete email templates for campaigns.

To use this app you have to setup an email client and install all required packages.

## Dashboard
On the main dashboard are widgets with the total number of campaigns and customers in the app. There is also a daily limit for emails, which can be sent to customers per day. This limit is reset every day and is based on the limit of the email client, which is used in the app.

![Dashboard](https://github.com/skapis/appscreenshots/blob/main/Campaign%20Manager/Dashboard.png)

## Campaign Dashboard
On campaign dashboard user can browse all campaigns in app. User can also use bulk insert to create more campaigns from csv file. Each campaign can be enabled or disabled. If the campaign is disabled it is not possible to send email to customers in this campaign.

![Campaign Dashboard](https://github.com/skapis/appscreenshots/blob/main/Campaign%20Manager/Campaign_Dashboard.png)

## Campaign Detail
In campaign detail, the user can edit, delete, enable or disable the campaign. Users can send emails to the customers if the campaign has at least one customer. There is also a log of emails, which were sent to customers.

![Campaign Detail](https://github.com/skapis/appscreenshots/blob/main/Campaign%20Manager/Campaign_Detail.png)

## Customers Dashboard
On the customers dashboard user can browse all customers in the app, create new ones, and edit or delete existing ones. It is also possible to import new customers by a csv file.

![Customer Dashboard](https://github.com/skapis/appscreenshots/blob/main/Campaign%20Manager/Customer_Dashboard.png)

![Customer detail](https://github.com/skapis/appscreenshots/blob/main/Campaign%20Manager/Customer_Detail.png)

## Email Template Dashboard
On the template dashboard user can create, edit or delete email templates. These templates are used for dynamic content for emails. The design of the template is not possible to change. If you want to change the design of the template not only the content, subject or header you must create a new html file and then assign it to the template in the Django administration.

![Template Dashboard](https://github.com/skapis/appscreenshots/blob/main/Campaign%20Manager/Template_Dashboard.png)

![Template Detail](https://github.com/skapis/appscreenshots/blob/main/Campaign%20Manager/Template_Detail.png)



