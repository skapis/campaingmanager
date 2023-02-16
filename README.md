# Campaing Manager
In this repository is simple app for manage campaigns and customers. This app is developed in Django Framework and it uses also JQuery. This app is based on three main instances, customers, campaigns and email templates. User can create, edit or delete customers and add them in to campaigns and then send them emails. Each customer can be add into one or more campaigns. Each campaign can have one current email template. User can create, edit or delete email templates for campaigns.

## Dashboard
On main dashboard are widgets with total number of campaigns and customers in app. There is also a daily limit for emails, which can be send to customers per day. This limit reset every day and is based on limit of email client, which is used in app.

![Dashboard](https://github.com/skapis/appscreenshots/blob/main/Campaign%20Manager/Dashboard.png)

## Campaign Dashboard
On campaign dashboard user can browse all campaigns in app. User can also use bulk insert to create more campaigns from csv file. Each campaign can be enabled or disabled. If the campaign is disabled it is not possible to send email to customers in this campaign.

![Campaign Dashboard](https://github.com/skapis/appscreenshots/blob/main/Campaign%20Manager/Campaign_Dashboard.png)

## Campaign Detail
In campaign detail user can edit, delete, enable or disable campaign. User can send there emails to customer, if campaign has at least one customer. There is also log of email, which were send to customers.

![Campaign Detail](https://github.com/skapis/appscreenshots/blob/main/Campaign%20Manager/Campaign_Detail.png)
