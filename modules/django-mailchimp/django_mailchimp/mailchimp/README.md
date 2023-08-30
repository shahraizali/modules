## Django Mailchimp backend configuration and information

## Module description

The module allow user to build custom features related to campaign, members, manage segments and target audiences and
templates.

The following are the features in scope for this module:

- Create a new campaign folder.
- Get & Update information about a specific folder used to organize campaigns.
- Give all campaigns in an account
- Create a new Mailchimp campaign.
- Add a new store to the user's Mailchimp account.
- Give information about all lists in the account.
- Give information about members in a specific Mailchimp list.
- Give information about list members who unsubscribed from a specific campaign.
- Give all folders used to organize templates.

## Features

- [ ] This module includes migrations.
- [x] This module includes environment variables.
- [x] This module requires manual configurations.
- [ ] This module can be configured with module options.

## Environment variables

```dotenv
MAILCHIMP_API_KEY="<API_KEY>"
MAILCHIMP_SERVER_REGION="<SERVER_REGION>"
```

## 3rd party setup

Create `Mailchimp Developers Account`

- Create MailChimp Developer account.
- Activate Mailchimp Account from the mail sent to user's provided email.
- Once the developer account is successfully created open the MailChimp Dashboard > On Lower Left corner of Side Bar
  Click on 'User Profile' Logo.
- Click 'Profile'.
- Click 'Extras' > Click 'API keys'. > Scroll the page down > Click 'Create A Key'.
  ![screenshot-us21 admin mailchimp com-2023 03 24-14_48_30](https://user-images.githubusercontent.com/120275623/227486815-2987705e-3dd4-4b22-bf65-c4cf95a9920b.png)

## Dependencies

[Mailchimp-Marketing](https://github.com/mailchimp/mailchimp-marketing-python/blob/master/README.md)

Dependencies used:

- [mailchimp-marketing=3.0.80](https://pypi.org/project/mailchimp-marketing/)

## API details

| Api Name                                                                                |                                              Param                                              | Description                                                                                                                                                                                                                            |
|-----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/modules/mailchimp/audience/{id}/add-list-member/` `POST`                              |                                      path_params `list_id`                                      | Add a new member to the list.                                                                                                                                                                                                          |
| `/modules/mailchimp/audience/{id}/add-or-remove-member-tag/{subscriber_hash}/` `POST`   | path_params `list_id`, `subscriber_hash` <br/> [Payload](#Postman-Collection-of-Mailchimp-APIs) | Add or remove tags from a list member                                                                                                                                                                                                  |
| `/modules/mailchimp/audience/{id}/add-segment/` `POST`                                  |                                      path_params `list_id`                                      | Create a new segment in a specific list.Required the request body. For details about request body visit the given link  https://mailchimp.com/developer/marketing/api/list-segments/add-segment/                                       |
| `/modules/mailchimp/audience/{id}/batch-subscribe-unsubscribe-audience/` `POST`         |                                      path_params `list_id`                                      | Batch subscribe or unsubscribe list members.Required the request body. For details about request body visit the given link . https://mailchimp.com/developer/marketing/api/lists/batch-subscribe-or-unsubscribe/                       |
| `/modules/mailchimp/audience/{id}/delete-audience-list/` `DELETE`                       |                                      path_params `list_id`                                      | Delete a list from Mailchimp account.                                                                                                                                                                                                  |
| `/modules/mailchimp/audience/{id}/delete-list-member/{subscriber_hash}/` `DELETE`       |                            path_params `list_id`, `subscriber_hash`                             | Delete all personally identifiable information related to a list member, and remove them from a list.This will make it impossible to re-import the list member.                                                                        |
| `/modules/mailchimp/audience/{id}/delete-segment/{segment_id}/` `DELETE`                |                               path_params `list_id`, `segment_id`                               | Delete a specific segment in a list.                                                                                                                                                                                                   |
| `/modules/mailchimp/audience/{id}/get-audience-list/`  `GET`                            |                                      path_params `list_id`                                      | Provide information about a specific list in Mailchimp account.                                                                                                                                                                        |
| `/modules/mailchimp/audience/{id}/get-member-info/{subscriber_hash}/` `GET`             |                            path_params `list_id`, `subscriber_hash`                             | Get information about a specific list member, including a currently subscribed, unsubscribed, or bounced member.                                                                                                                       |
| `/modules/mailchimp/audience/{id}/get-segment-info/{segment_id}/` `GET`                 |                               path_params `list_id`, `segment_id`                               | Get information about a specific segment.                                                                                                                                                                                              |
| `/modules/mailchimp/audience/{id}/list-member-info/`  `GET`                             |                            path_params `list_id`, `subscriber_hash`                             | Get information about members in a specific Mailchimp list.                                                                                                                                                                            |
| `/modules/mailchimp/audience/{id}/list-member-tags/{subscriber_hash}/`  `GET`           |                            path_params `list_id`, `subscriber_hash`                             | Provide the tags on a list member.                                                                                                                                                                                                     |
| `/modules/mailchimp/audience/{id}/list-segment/`   `GET`                                |                                      path_params `list_id`                                      | Provide information about all available segments for a specific list.                                                                                                                                                                  |
| `/modules/mailchimp/audience/{id}/update-audience-list/` `POST`                         |             path_params `list_id`, [Payload](#Postman-Collection-of-Mailchimp-APIs)             | Update a specific segment in a list.Required the request body. For details about request body visit the given link . https://mailchimp.com/developer/marketing/api/list-segments/update-segment/                                       |
| `/modules/mailchimp/audience/{id}/update-list-member/{subscriber_hash}/` `POST`         |   path_params `list_id`, `subscriber_hash`, [Payload](#Postman-Collection-of-Mailchimp-APIs)    | Update information for a specific list member.                                                                                                                                                                                         |
| `/modules/mailchimp/audience/{id}/update-segment/{segment_id}/` `POST`                  |      path_params `list_id`, `segment_id`, [Payload](#Postman-Collection-of-Mailchimp-APIs)      | Update a specific segment in a list.Required the request body. For details about request body visit the given link .https://mailchimp.com/developer/marketing/api/list-segments/update-segment/                                        |
| `/modules/mailchimp/audience/add-audience-list/` `POST`                                 |                        [Payload](#Postman-Collection-of-Mailchimp-APIs)                         | Create a new list in Mailchimp account.Required the request body. For details about request body visit the given link .https://mailchimp.com/developer/marketing/api/lists/add-list/                                                   |
| `/modules/mailchimp/audience/get-audience-lists/` `GET`                                 |                                              None                                               | Provide information about all lists in the account.User can use optional query Parameters. For details about query Parameters visit the given link .https://mailchimp.com/developer/marketing/api/lists/get-lists-info/                |
| `/modules/mailchimp/campaign-reports/{id}/get-campaign-abuse-report/{report_id}/` `GET` |                             path_params `campaign_id`, `report_id`                              | Get information about a specific abuse report for a campaign.                                                                                                                                                                          |
| `/modules/mailchimp/campaign-reports/{id}/get-campaign-abuse-reports/`  `GET`           |                                    path_params `campaign_id`                                    | Get a list of abuse complaints for a specific campaign.                                                                                                                                                                                |
| `/modules/mailchimp/campaign-reports/{id}/get-campaign-click-details/`   `GET`          |                                    path_params `campaign_id`                                    | Get information about clicks on specific links in your Mailchimp campaigns.                                                                                                                                                            |
| `/modules/mailchimp/campaign-reports/{id}/get-campaign-open-details/`  `GET`            |                                    path_params `campaign_id`                                    | Get detailed information about any campaign emails that were opened by a list member.                                                                                                                                                  |
| `/modules/mailchimp/campaign-reports/{id}/get-campaign-report/`  `GET`                  |                                    path_params `campaign_id`                                    | Get report details for a specific sent campaign.                                                                                                                                                                                       |
| `/modules/mailchimp/campaign-reports/list-campaign-report/`   `GET`                     |                                              None                                               | Get campaign reports.                                                                                                                                                                                                                  |
| `/modules/mailchimp/campaigns/{id}/cancel-campaign/`  `POST`                            |                                    path_params `campaign_id`                                    | Cancel a Regular or Plain-Text Campaign after you send, before all of your recipients receive it. This feature is included with Mailchimp Pro.                                                                                         |
| `/modules/mailchimp/campaigns/{id}/delete-campaign/` `DELETE`                           |                                    path_params `campaign_id`                                    | Remove a campaign from your Mailchimp account.                                                                                                                                                                                         |
| `/modules/mailchimp/campaigns/{id}/get-campaign-folder/` `GET`                          |                                     path_params `folder_id`                                     | Get information about a specific folder used to organize campaigns.Required the request body. For details about request body visit the given link .https://mailchimp.com/developer/marketing/api/campaign-folders/get-campaign-folder/ |
| `/modules/mailchimp/campaigns/{id}/get-campaign-info/`   `GET`                          |                                    path_params `campaign_id`                                    | Get information about a specific campaign.                                                                                                                                                                                             |
| `/modules/mailchimp/campaigns/{id}/send-campaign/` `POST`                               |                                    path_params `campaign_id`                                    | Send a Mailchimp campaign. For RSS Campaigns, the campaign will send according to its schedule. All other campaigns will send immediately.                                                                                             |
| `/modules/mailchimp/campaigns/{id}/unschedule-campaign/` `POST`                         |                                    path_params `campaign_id`                                    | Unschedule a scheduled campaign that hasn't started sending.Required the request body. For details about request body visit the given link .https://mailchimp.com/developer/marketing/api/campaigns/unschedule-campaign/               |
| `/modules/mailchimp/campaigns/{id}/update-campaign-folder/`  `POST`                     |            path_params `folder_id`, [Payload](#Postman-Collection-of-Mailchimp-APIs)            | Update a specific folder used to organize campaigns.Required the request body. For details about request body visit the given link .https://mailchimp.com/developer/marketing/api/campaign-folders/update-campaign-folder/             |
| `/modules/mailchimp/campaigns/{id}/update-campaign-settings/`  `POST`                   |           path_params `campaign_id`, [Payload](#Postman-Collection-of-Mailchimp-APIs)           | Update some or all of the settings for a specific campaign.Required the request body. For details about request body visit the given link .https://mailchimp.com/developer/marketing/api/campaigns/update-campaign-settings/           |
| `/modules/mailchimp/campaigns/add-campaign-folder/`   `POST`                            |                        [Payload](#Postman-Collection-of-Mailchimp-APIs)                         | Create a new campaign folder.Required the request body. For details about request body visit the given link .https://mailchimp.com/developer/marketing/api/campaign-folders/add-campaign-folder/                                       |
| `/modules/mailchimp/campaigns/add-campaigns/`   `POST`                                  |                        [Payload](#Postman-Collection-of-Mailchimp-APIs)                         | Create a new Mailchimp campaign.Required the request body. For details about request body visit the given link .https://mailchimp.com/developer/marketing/api/campaigns/add-campaign/                                                  |
| `/modules/mailchimp/campaigns/list-campaign-folder/`  `GET`                             |                                              None                                               | Get all folders used to organize campaigns.                                                                                                                                                                                            |
| `/modules/mailchimp/campaigns/list-campaigns/`   `GET`                                  |                                              None                                               | Get all campaigns in an account.                                                                                                                                                                                                       |
| `/modules/mailchimp/templates/{id}/delete-template/`  `DELETE`                          |                                    path_params `template_id`                                    | Delete a specific template.                                                                                                                                                                                                            |
| `/modules/mailchimp/templates/{id}/delete-template-folder/`  `DELETE`                   |                                     path_params `folder_id`                                     | Delete a specific template folder, and mark all the templates in the folder as 'unfilled'.                                                                                                                                             |
| `/modules/mailchimp/templates/{id}/get_template_info/`   `GET`                          |                                    path_params `template_id`                                    | Get information about a specific template.                                                                                                                                                                                             |
| `/modules/mailchimp/templates/{id}/update-template/`  `POST`                            |           path_params`template_id` , [Payload](#Postman-Collection-of-Mailchimp-APIs)           | Update the name, HTML, or folder_id of an existing template.Required the request body. For details about request body visit the given link .https://mailchimp.com/developer/marketing/api/templates/update-template/                   |
| `/modules/mailchimp/templates/{id}/update-template-folder/` `POST`                      |            path_params `folder_id`, [Payload](#Postman-Collection-of-Mailchimp-APIs)            | Update a specific folder used to organize templates.Required the request body. For details about request body visit the given link .https://mailchimp.com/developer/marketing/api/template-folders/update-template-folder/             |
| `/modules/mailchimp/templates/add-template/`   `POST`                                   |                        [Payload](#Postman-Collection-of-Mailchimp-APIs)                         | Create a new template for the account. Only Classic templates are supported.Required the request body. For details about request body visit the given link .https://mailchimp.com/developer/marketing/api/templates/add-template/      |
| `/modules/mailchimp/templates/add-template-folder/`  `POST`                             |                        [Payload](#Postman-Collection-of-Mailchimp-APIs)                         | Create a new template folder.Required the request body. For details about request body visit the given link .https://mailchimp.com/developer/marketing/api/template-folders/add-template-folder/                                       |
| `/modules/mailchimp/templates/list-template/` `GET`                                     |                                              None                                               | Get a list of an account's available templates.                                                                                                                                                                                        |
| `/modules/mailchimp/templates/list-template-folder/`  `GET`                             |                                              None                                               | Get all folders used to organize templates.                                                                                                                                                                                            |                                                                                          |

## Postman Collection of Mailchimp APIs

Here is a collection of all the api endpoints for the mailchimp module.
[Mailchimp-APIs Postman Collection](https://drive.google.com/file/d/1kzci3MH3eVcxX6nniaDQOSaeHQe24xFD/view?usp=share_link)
