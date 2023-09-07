from unittest import mock

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import StripeUserProfile, StripeSetting, UserSubscription, AppleIAPProduct

User = get_user_model()


class PaymentSheetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john34@gmail.com', password='john123@')
        self.token = Token.objects.create(user=self.user)
        self.stripe_user = User.objects.create_user(username='david', email='david4@gmail.com', password='david123@')
        self.stripe_user_token = Token.objects.create(user=self.stripe_user)
        self.stripe_setting = StripeSetting.objects.create(user=self.stripe_user)
        self.stripe_setting_user = User.objects.create_user(username='alan', email='alan4@gmail.com',
                                                            password='alan123@')
        self.stripe_setting_user_token = Token.objects.create(user=self.stripe_setting_user)
        self.stripe_setting = StripeSetting.objects.create(user=self.stripe_setting_user, is_wallet_connect=True)

    @mock.patch('modules.payments.payments.services.stripe_payments.stripe.Customer.create')
    @mock.patch('modules.payments.payments.services.stripe_payments.StripeService.create_payment_intent_sheet')
    def test_create_payment_intent(self, create_payment_intent_sheet_mock, stripe_customer_create_mock):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        mock_response = dict(paymentIntent='pi_3MRXEOsadhegdyexss',
                             ephemeralKey='ek_test_YWNjdF8xTVJXzjdhfdjdcjQ2dThFQmRkbGpDb',
                             customer='cus_demoos3dsd342ds23d')
        create_payment_intent_sheet_mock.return_value = mock_response
        stripe_customer_create_mock.return_value = {"id": "cus_demoos3dsd342ds23d"}
        url = '/modules/payments/create_payment_intent_sheet/'
        response = self.client.post(url, format='json')
        self.assertEqual(mock_response['paymentIntent'], response.data['paymentIntent'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        create_payment_intent_sheet_mock.assert_called_once()
        create_payment_intent_sheet_mock.assert_called_once_with(response.data['customer'], 100)

    @mock.patch('modules.payments.payments.services.stripe_payments.stripe.Customer.create')
    @mock.patch('modules.payments.payments.services.stripe_payments.StripeService.create_payment_intent_sheet')
    def test_create_payment_intent_with_stripe_setting(self, create_payment_intent_sheet_mock,
                                                       stripe_customer_create_mock):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.stripe_user_token.key)
        mock_response = dict(paymentIntent='pi_3MRXEOHocl234wo2ilpC0dsf32me7kH_demo_2iOQZgcjjEs6I9rlRw73bK',
                             ephemeralKey='ek_test_demo3et637v5cvs36s62a2avg2ge67wav2662z2',
                             customer='cus_demoos3dsd342ds23d')
        create_payment_intent_sheet_mock.return_value = mock_response
        stripe_customer_create_mock.return_value = {"id": "cus_demoos3dsd342ds23d"}
        url = '/modules/payments/create_payment_intent_sheet/'
        response = self.client.post(url, format='json')
        self.assertEqual(mock_response['paymentIntent'], response.data['paymentIntent'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        create_payment_intent_sheet_mock.assert_called_once()
        create_payment_intent_sheet_mock.assert_called_once_with(response.data['customer'], 100)

    @mock.patch('modules.payments.payments.services.stripe_payments.stripe.Customer.create')
    @mock.patch('modules.payments.payments.services.stripe_payments.StripeService.create_payment_intent_sheet')
    def test_create_payment_intent_with_stripe_setting_wallet_connect(self, create_payment_intent_sheet_mock,
                                                                      stripe_customer_create_mock):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.stripe_setting_user_token.key)
        mock_response = dict(paymentIntent='pi_demo decode7823teg3db3ws_2iOQZgcjjEs6I9rlREMMw73bK',
                             ephemeralKey='ek_test_demo3et637v5cvs36s62a2avg2ge67fwav2662z2',
                             customer='cus_demoos3dsd342ds23d')
        create_payment_intent_sheet_mock.return_value = mock_response
        stripe_customer_create_mock.return_value = {"id": "cus_demoos3dsd342ds23d"}
        url = '/modules/payments/create_payment_intent_sheet/'
        response = self.client.post(url, format='json')
        self.assertEqual(mock_response['paymentIntent'], response.data['paymentIntent'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        create_payment_intent_sheet_mock.assert_called_once()

    @mock.patch('modules.payments.payments.services.stripe_payments.stripe.Customer.create')
    @mock.patch('modules.payments.payments.services.stripe_payments.StripeService.create_payment_intent_sheet')
    def test_create_payment_intent_with_stripe_customer_id(self, create_payment_intent_sheet_mock,
                                                           stripe_customer_create_mock):
        new_user = User.objects.create(username='wick', email='wick77@gmail.com', password='wick123@')
        tokens = Token.objects.create(user=new_user)
        stripe_profile, created = StripeUserProfile.objects.get_or_create(user_id=new_user.pk)
        if not created:
            stripe_profile.stripe_cus_id = "cus_demoos3dsd342ds23d"
            stripe_profile.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tokens.key)
        mock_response = {'paymentIntent': 'pi_demo decode7823teg3db3ws_2iOQZgcjjEs6I9rlREMMw73bK',
                         'ephemeralKey': 'ek_test_demo3et637v5cvs36s62a2avg2ge67fwav2662z2',
                         'customer': 'cus_demoos3dsd342ds23d'}
        create_payment_intent_sheet_mock.return_value = mock_response
        stripe_customer_create_mock.return_value = {"id": "cus_demoos3dsd342ds23d"}
        url = '/modules/payments/create_payment_intent_sheet/'
        response = self.client.post(url, format='json')
        self.assertEqual(mock_response['paymentIntent'], response.data['paymentIntent'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        create_payment_intent_sheet_mock.assert_called_once()
        create_payment_intent_sheet_mock.assert_called_once_with(response.data['customer'], 100)

    def test_create_payment_intent_without_authorization(self):
        url = '/modules/payments/create_payment_intent_sheet/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_payment_intent_without_stripe_profile(self):
        self.get_user = User.objects.create(username='wick', email='wick77@gmail.com', password='wick123@')
        tokens = Token.objects.create(user=self.get_user)
        StripeUserProfile.objects.get(user=self.get_user).delete()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tokens.key)
        url = '/modules/payments/create_payment_intent_sheet/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetStripePaymentsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='david', email='david77@gmail.com', password='david123@')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @mock.patch('modules.payments.payments.services.stripe_payments.StripeService.get_payments_history')
    def test_get_stripe_payments_history(self, get_stripe_payments_mock):
        mock_response = {
            "success": True,
            "data": [
                {
                    "id": "pi_3MRXEOSophoclesC0able7kH",
                    "object": "payment_intent",
                    "amount": 100,
                    "amount_capturable": 0,
                    "amount_details": {
                        "tip": {}
                    },
                    "amount_received": 0,
                    "capture_method": "automatic",
                    "client_secret": "pi_demo decode7823teg3db3ws_2iOQZgcjjEs6I9rlREMMw73bK",
                    "confirmation_method": "automatic",
                    "created": 1674031372,
                    "currency": "usd",
                    "customer": "cus_demoos3dsd342ds23d",
                    "payment_method_options": {
                        "card": {
                            "request_three_d_secure": "automatic"
                        }
                    },
                    "payment_method_types": [
                        "card"
                    ],
                    "status": "requires_payment_method",
                }
            ]
        }
        get_stripe_payments_mock.return_value = mock_response
        url = '/modules/payments/get_payments_history/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['data'], mock_response['data'])
        self.assertEqual(response.data['data']['data'][0], mock_response['data'][0])
        self.assertEqual(response.data['success'], mock_response['success'])
        get_stripe_payments_mock.assert_called_once()
        get_stripe_payments_mock.assert_called_once_with(None)

    @mock.patch('modules.payments.payments.services.stripe_payments.StripeService.get_payments_history')
    def test_get_stripe_payments_history_with_user_stripe_customer_id(self, get_stripe_payments_mock):
        new_user = User.objects.create(username='wick', email='wick77@gmail.com', password='wick123@')
        tokens = Token.objects.create(user=new_user)
        stripe_profile, created = StripeUserProfile.objects.get_or_create(user_id=new_user.pk)
        if not created:
            stripe_profile.stripe_cus_id = "cus_demoos3dsd342ds23d"
            stripe_profile.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tokens.key)
        mock_response = {
            "success": True,
            "data": [
                {
                    "id": "pi_3MRXEOSophoclesC0able7kH",
                    "object": "payment_intent",
                    "amount": 100,
                    "amount_capturable": 0,
                    "amount_details": {
                        "tip": {}
                    },
                    "amount_received": 0,
                    "capture_method": "automatic",
                    "client_secret": "pi_demo decode7823teg3db3ws_2iOQZgcjjEs6I9rlREMMw73bK",
                    "confirmation_method": "automatic",
                    "created": 1674031372,
                    "currency": "usd",
                    "customer": "cus_demoos3dsd342ds23d",
                    "payment_method_options": {
                        "card": {
                            "request_three_d_secure": "automatic"
                        }
                    },
                    "payment_method_types": [
                        "card"
                    ],
                    "status": "requires_payment_method",
                }
            ]
        }
        get_stripe_payments_mock.return_value = mock_response
        url = '/modules/payments/get_payments_history/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['data'], mock_response['data'])
        self.assertEqual(response.data['data']['data'][0], mock_response['data'][0])
        self.assertEqual(response.data['success'], mock_response['success'])
        get_stripe_payments_mock.assert_called_once()
        get_stripe_payments_mock.assert_called_once_with("cus_demoos3dsd342ds23d")

    @mock.patch('modules.payments.payments.services.stripe_payments.StripeService.get_payments_history')
    def test_get_stripe_payments_history_without_authorization(self, get_stripe_payments_mock):
        self.client.force_authenticate(user=None, token=None)
        mock_response = None
        get_stripe_payments_mock.return_value = mock_response
        url = '/modules/payments/get_payments_history/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_payment_history_without_stripe_profile(self):
        self.get_user = User.objects.create(username='wicks', email='wicks77@gmail.com', password='wicks123@')
        tokens = Token.objects.create(user=self.get_user)
        StripeUserProfile.objects.get(user=self.get_user).delete()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tokens.key)
        url = '/modules/payments/get_payments_history/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetPaymentMethodsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='david', email='david77@gmail.com', password='david123@')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @mock.patch('modules.payments.payments.services.stripe_payments.StripeService.get_payments_methods')
    def test_get_payments_methods(self, get_payments_methods_mock):
        mock_response = {'success': True, 'data': []}
        get_payments_methods_mock.return_value = mock_response
        url = '/modules/payments/get_payments_methods/'
        response = self.client.get(url)
        self.assertEqual(response.data['success'], mock_response['success'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        get_payments_methods_mock.assert_called_once()
        get_payments_methods_mock.assert_called_once_with(None)

    @mock.patch('modules.payments.payments.services.stripe_payments.StripeService.get_payments_methods')
    def test_get_payments_methods_with_user_stripe_customer_id(self, get_payments_methods_mock):
        new_user = User.objects.create(username='wick', email='wick77@gmail.com', password='wick123@')
        tokens = Token.objects.create(user=new_user)
        stripe_profile, created = StripeUserProfile.objects.get_or_create(user_id=new_user.pk)
        if not created:
            stripe_profile.stripe_cus_id = "cus_demoos3dsd342ds23d"
            stripe_profile.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tokens.key)
        mock_response = {'success': True, 'data': []}
        get_payments_methods_mock.return_value = mock_response
        url = '/modules/payments/get_payments_methods/'
        response = self.client.get(url)
        self.assertEqual(response.data['success'], mock_response['success'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        get_payments_methods_mock.assert_called_once()
        get_payments_methods_mock.assert_called_once_with("cus_demoos3dsd342ds23d")

    @mock.patch('modules.payments.payments.services.stripe_payments.StripeService.get_payments_methods')
    def test_get_payments_methods_without_authorization(self, get_payments_methods_mock):
        self.client.force_authenticate(user=None, token=None)
        mock_response = None
        get_payments_methods_mock.return_value = mock_response
        url = '/modules/payments/get_payments_methods/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_payment_method_without_stripe_profile(self):
        self.get_user = User.objects.create(username='vicky', email='vicky77@gmail.com', password='vicky123@')
        tokens = Token.objects.create(user=self.get_user)
        StripeUserProfile.objects.get(user=self.get_user).delete()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tokens.key)
        url = '/modules/payments/get_payments_methods/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetSubscriptionPlanTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user', email='test_user77@gmail.com', password='test123@')
        self.token = Token.objects.create(user=self.user)

    def test_get_subscription_plans(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/modules/payments/get_subscription_plans/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)

    def test_get_subscription_plans_without_authorization(self):
        url = '/modules/payments/get_subscription_plans/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BuySubscriptionPlanTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='plan_user', email='plan_user77@gmail.com', password='plan123@')
        self.token = Token.objects.create(user=self.user)

    @mock.patch('modules.payments.payments.viewsets.SubscriptionPlan')
    @mock.patch('modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.already_has_a_plan')
    @mock.patch('modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.get_price_details')
    @mock.patch('modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.update_subscription')
    @mock.patch('modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.create_subscription')
    @mock.patch('modules.payments.payments.services.stripe_payments.stripe.Customer.create')
    def test_buy_subscription_with_already_has_a_plan(self, stripe_customer_create_mock, create_subscription_mock,
                                                      update_subscription_mock, get_price_details_mock,
                                                      already_has_a_plan_mock, subscriptionPlan_mock):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        stripe_profile, created = StripeUserProfile.objects.get_or_create(user_id=self.user.pk)
        if not created:
            stripe_profile.stripe_cus_id = "cus_demoos3dsd342ds23d"
            stripe_profile.save()

        mock_response = {
            "id": "sub_demo236533s",
            "object": "subscription",
            "collection_method": "charge_automatically",
            "created": 1693938080,
            "currency": "usd",
            "current_period_end": 1696530080,
            "current_period_start": 1693938080,
            "customer": "cus_demo-au63t6td",
            "default_payment_method": "pm_demo2as4edged33",
            "default_tax_rates": [],
            "items": {
                "object": "list",
                "data": [
                    {
                        "id": "si_sadb326ws",
                        "object": "subscription_item",
                        "created": 1693938080,
                        "metadata": {},
                        "plan": {
                            "id": "price_sdu3y7e33ssa",
                            "object": "plan",
                            "amount": 800,
                            "created": 1619020781,
                            "currency": "usd",
                            "product": "prod_demo3e3s2s2s",
                            "trial_period_days": 7,
                            "usage_type": "licensed"
                        },
                        "price": {
                            "id": "price_sdu3y7e33ssa",
                            "object": "price",
                            "billing_scheme": "per_unit",
                            "created": 1619020781,
                            "currency": "usd",
                            "product": "prod_demo3e3s2s2s",
                            "recurring": {
                                "interval": "month",
                                "interval_count": 1,
                                "trial_period_days": 7,
                            },
                            "tax_behavior": "unspecified",
                            "type": "recurring",
                            "unit_amount": 800,
                            "unit_amount_decimal": "800"
                        },
                        "quantity": 1,
                        "subscription": "sub_demo3e7sgy2gs",
                        "tax_rates": []
                    }
                ],
                "total_count": 1,
                "url": "/v1/subscription_items?subscription=sub_1Nn3sKBZuKMpaGSnx87G3ET"
            },
            "latest_invoice": "in_dye3td3sgsssa",
            "plan": {
                "id": "price_sdu3y7e33ssa",
                "object": "plan",
                "amount": 800,
                "created": 1619020781,
                "currency": "usd",
                "interval": "month",
                "interval_count": 1,
                "product": "prod_demo3e3s2s2s",
                "trial_period_days": 7,
                "usage_type": "licensed"
            },
            "quantity": 1,
            "start_date": 1693938080,
            "status": "active",
            "trial_settings": {
                "end_behavior": {
                    "missing_payment_method": "create_invoice"
                }
            },
        }
        create_subscription_mock.return_value = mock_response
        update_subscription_mock.return_value = mock_response
        get_price_details_mock.return_value = {"id": "price_sdu3y7e33ssa", "unit_amount": 8, "type": "recurring",
                                               "interval": "month"}
        self.user_subscription = UserSubscription.objects.create(user=self.user,
                                                                 subscription_id="cus_demoos3dsd342ds23d")
        stripe_customer_create_mock.return_value = self.user
        already_has_a_plan_mock.return_value = self.user_subscription
        subscriptionPlan_mock.return_value = {"price_id": "price_sdu3y7e33ssa", "name": 'SUB MEALS 1', "price": 8,
                                              "plan_type": "recurring", "interval": "month"}

        url = '/modules/payments/buy_subscription_plan/'
        data = {
            "price_tier": "price_sdu3y7e33ssa"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], mock_response['id'])
        update_subscription_mock.assert_called_once()

    @mock.patch('modules.payments.payments.viewsets.SubscriptionPlan')
    @mock.patch('modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.already_has_a_plan')
    @mock.patch('modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.get_price_details')
    @mock.patch('modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.update_subscription')
    @mock.patch('modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.create_subscription')
    @mock.patch('modules.payments.payments.services.stripe_payments.stripe.Customer.create')
    def test_buy_subscription_without_already_has_a_plan(self, stripe_customer_create_mock, create_subscription_mock,
                                                         update_subscription_mock, get_price_details_mock,
                                                         already_has_a_plan_mock, subscriptionPlan_mock):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        mock_response = {
            "id": "sub_demo236533s",
            "object": "subscription",
            "collection_method": "charge_automatically",
            "created": 1693938080,
            "currency": "usd",
            "current_period_end": 1696530080,
            "current_period_start": 1693938080,
            "customer": "cus_demo-au63t6td",
            "default_payment_method": "pm_demo2as4edged33",
            "default_tax_rates": [],
            "items": {
                "object": "list",
                "data": [
                    {
                        "id": "si_sadb326ws",
                        "object": "subscription_item",
                        "created": 1693938080,
                        "metadata": {},
                        "plan": {
                            "id": "price_sdu3y7e33ssa",
                            "object": "plan",
                            "amount": 800,
                            "created": 1619020781,
                            "currency": "usd",
                            "product": "prod_demo3e3s2s2s",
                            "trial_period_days": 7,
                            "usage_type": "licensed"
                        },
                        "price": {
                            "id": "price_sdu3y7e33ssa",
                            "object": "price",
                            "billing_scheme": "per_unit",
                            "created": 1619020781,
                            "currency": "usd",
                            "product": "prod_demo3e3s2s2s",
                            "recurring": {
                                "interval": "month",
                                "interval_count": 1,
                                "trial_period_days": 7,
                            },
                            "tax_behavior": "unspecified",
                            "type": "recurring",
                            "unit_amount": 800,
                            "unit_amount_decimal": "800"
                        },
                        "quantity": 1,
                        "subscription": "sub_demo3e7sgy2gs",
                        "tax_rates": []
                    }
                ],
                "total_count": 1,
                "url": "/v1/subscription_items?subscription=sub_1Nn3sKBZuKMpaGSnx87G3ET"
            },
            "latest_invoice": "in_dye3td3sgsssa",
            "plan": {
                "id": "price_sdu3y7e33ssa",
                "object": "plan",
                "amount": 800,
                "created": 1619020781,
                "currency": "usd",
                "interval": "month",
                "interval_count": 1,
                "product": "prod_demo3e3s2s2s",
                "trial_period_days": 7,
                "usage_type": "licensed"
            },
            "quantity": 1,
            "start_date": 1693938080,
            "status": "active",
            "trial_settings": {
                "end_behavior": {
                    "missing_payment_method": "create_invoice"
                }
            },
        }
        create_subscription_mock.return_value = mock_response
        update_subscription_mock.return_value = mock_response
        get_price_details_mock.return_value = {"id": "price_sdu3y7e33ssa", "unit_amount": 8, "type": "recurring",
                                               "interval": "month"}
        self.user_subscription = UserSubscription.objects.create(user=self.user,
                                                                 subscription_id=None)
        stripe_customer_create_mock.return_value = {"id": None}
        already_has_a_plan_mock.return_value = self.user_subscription
        subscriptionPlan_mock.return_value = {"price_id": "price_sdu3y7e33ssa", "name": 'SUB MEALS 1', "price": 8,
                                              "plan_type": "recurring", "interval": "month"}

        url = '/modules/payments/buy_subscription_plan/'
        data = {
            "price_tier": "price_sdu3y7e33ssa"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], mock_response['id'])
        create_subscription_mock.assert_called_once()


class CancelSubscriptionPlanTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='plan_user', email='plan_user77@gmail.com', password='plan123@')
        self.token = Token.objects.create(user=self.user)

    @mock.patch('modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.already_has_a_plan')
    @mock.patch('modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.cancel_subscription')
    def test_cancel_subscription(self, cancel_subscription_mock, already_has_a_plan_mock):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.user_subscription = UserSubscription.objects.create(user=self.user,
                                                                 subscription_id="cus_demoos3dsd342ds23d")
        already_has_a_plan_mock.return_value = self.user_subscription
        cancel_subscription_mock.return_value = {
            "application": None,
            "application_fee_percent": None,
            "automatic_tax": {
                "enabled": False
            },
            "billing_cycle_anchor": 1693938080,
            "cancellation_details": {
                "reason": "cancellation_requested"
            },
            "collection_method": "charge_automatically",
            "id": "sub_1Nn3sKBZuKMpaGSnx87G3ET",
            "items": {
                "data": [
                    {
                        "billing_thresholds": None,
                        "created": 1693938080,
                        "id": "si_OaELJd0jFThpZ",
                        "quantity": 1,
                        "subscription": "sub_demoBZuKMpaGSnx87G3ET",
                        "tax_rates": []
                    }
                ],
                "total_count": 1,
                "url": "/v1/subscription_items?subscription=sub_1Nn3sKBZuKMpaGSnx87G3ET"
            },
            "latest_invoice": "in_demoBZuKMpaGSqlYpHWcQ",
            "plan": {
                "usage_type": "licensed"
            },
            "quantity": 1,
            "trial_settings": {
                "end_behavior": {
                    "missing_payment_method": "create_invoice"
                }
            },
        }
        url = '/modules/payments/cancel_subscription_plan/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        already_has_a_plan_mock.assert_called_once()
        cancel_subscription_mock.assert_called_once()


class AppleIAProductsViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='plan_user', email='plan_user77@gmail.com', password='plan123@')
        self.token = Token.objects.create(user=self.user)
        self.apple_prod = AppleIAPProduct.objects.create(name="apple_test", product_id="prod_JLPHuHgB2Th9Ox",
                                                         is_active=True)

    def test_get_products(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/modules/payments/apple/get_products/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.apple_prod.name)
        self.assertEqual(response.data[0]['product_id'], self.apple_prod.product_id)
        self.assertEqual(response.data[0]['is_active'], self.apple_prod.is_active)

    @mock.patch('modules.payments.payments.services.apple_payments.ApplePaymentService.verify_apple_receipt')
    def test_verify_apple_with_valid_receipt_data(self, verify_apple_receipt_mock):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        mock_response = {'status': 21002}, True
        verify_apple_receipt_mock.return_value = mock_response
        url = '/modules/payments/apple/verify/receipt/'
        data = {
            "productId": self.apple_prod.product_id,
            "transactionDate": "oirjsl948jdjdl",
            "transactionId": "oiwueoja",
            "transactionReceipt": "kdsjoiejwlkj",
            "user": "test_user"
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        verify_apple_receipt_mock.assert_called_once()

    @mock.patch('modules.payments.payments.services.apple_payments.ApplePaymentService.verify_apple_receipt')
    def test_verify_apple_with_invalid_receipt_data(self, verify_apple_receipt_mock):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        verify_apple_receipt_mock.return_value = {'status': 21002}, False
        url = '/modules/payments/apple/verify/receipt/'
        data = {
            "productId": "sub_343TF",
            "transactionDate": "oirjsl948jdjdl",
            "transactionId": "oiwueoja",
            "transactionReceipt": "kdsjoiejwlkj",
            "user": "test_user"
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        verify_apple_receipt_mock.assert_called_once()


class StripeWebhookViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='plan_user', email='plan_user77@gmail.com', password='plan123@')
        self.token = Token.objects.create(user=self.user)

    @mock.patch(
        'modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.get_event_from_webhook')
    @mock.patch(
        'modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.handle_webhook_events')
    def test_post_webhook(self, get_event_from_webhook_mock, handle_webhook_events_mock):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        mock_response = {
            "api_version": "2023-08-16",
            "created": 1680064028,
            "data": {
                "object": {
                    "application": None,
                    "application_fee_percent": None,
                    "automatic_tax": {
                        "enabled": False
                    },
                    "billing_cycle_anchor": 1680668814,
                    "billing_thresholds": None,
                    "cancel_at": None,
                    "cancel_at_period_end": False,
                    "canceled_at": None,
                    "cancellation_details": {
                        "comment": None,
                        "feedback": None,
                        "reason": None
                    },
                    "collection_method": "charge_automatically",
                    "created": 1680064014,
                    "currency": "usd",
                    "current_period_end": 1683260814,
                    "current_period_start": 1680668814,
                    "customer": "cus_M09xxkyq9tmgOu",
                    "days_until_due": None,
                    "default_payment_method": None,
                    "default_source": None,
                    "default_tax_rates": [],
                    "description": "A test subscription",
                    "discount": None,
                    "ended_at": None,
                    "id": "sub_1Mqqb6Lt4dXK03v50OA219Ya",
                    "invoice_customer_balance_settings": {
                        "consume_applied_balance_on_void": True
                    },
                    "items": {
                        "data": [
                            {
                                "billing_thresholds": None,
                                "created": 1680064014,
                                "id": "si_Nc4kEcMHd3vRTS",
                                "metadata": {},
                                "object": "subscription_item",
                                "plan": {
                                    "active": True,
                                    "aggregate_usage": None,
                                    "amount": 4242,
                                    "amount_decimal": "4242",
                                    "billing_scheme": "per_unit",
                                    "created": 1680064015,
                                    "currency": "usd",
                                    "id": "price_1IiiSnBZuKMpoaGS1BSrP8Rs",
                                    "interval": "month",
                                    "interval_count": 1,
                                    "livemode": False,
                                    "metadata": {},
                                    "nickname": None,
                                    "object": "plan",
                                    "product": "prod_Nc4kjj2XYpywZV",
                                    "tiers": None,
                                    "tiers_mode": None,
                                    "transform_usage": None,
                                    "trial_period_days": None,
                                    "usage_type": "licensed"
                                },
                                "price": {
                                    "active": True,
                                    "billing_scheme": "per_unit",
                                    "created": 1680064015,
                                    "currency": "usd",
                                    "custom_unit_amount": None,
                                    "id": "price_1Mqqb5Lt4dXK03v5cK9prani",
                                    "livemode": False,
                                    "lookup_key": None,
                                    "metadata": {},
                                    "migrate_to": None,
                                    "nickname": None,
                                    "object": "price",
                                    "product": "prod_Nc4kjj2XYpywZV",
                                    "recurring": {
                                        "aggregate_usage": None,
                                        "interval": "month",
                                        "interval_count": 1,
                                        "trial_period_days": None,
                                        "usage_type": "licensed"
                                    },
                                    "tax_behavior": "unspecified",
                                    "tiers_mode": None,
                                    "transform_quantity": None,
                                    "type": "recurring",
                                    "unit_amount": 4242,
                                    "unit_amount_decimal": "4242"
                                },
                                "quantity": 1,
                                "subscription": "sub_1Mqqb6Lt4dXK03v50OA219Ya",
                                "tax_rates": []
                            }
                        ],
                        "has_more": False,
                        "object": "list",
                        "total_count": 1,
                        "url": "/v1/subscription_items?subscription=sub_1Mqqb6Lt4dXK03v50OA219Ya"
                    },
                    "latest_invoice": "in_1MqqbILt4dXK03v5cbbciqFZ",
                    "livemode": False,
                    "metadata": {},
                    "next_pending_invoice_item_invoice": None,
                    "object": "subscription",
                    "on_behalf_of": None,
                    "pause_collection": None,
                    "payment_settings": {
                        "payment_method_options": None,
                        "payment_method_types": None,
                        "save_default_payment_method": "off"
                    },
                    "pending_invoice_item_interval": None,
                    "pending_setup_intent": None,
                    "pending_update": None,
                    "plan": {
                        "active": True,
                        "aggregate_usage": None,
                        "amount": 4242,
                        "amount_decimal": "4242",
                        "billing_scheme": "per_unit",
                        "created": 1680064015,
                        "currency": "usd",
                        "id": "price_1IiiSnBZuKMpoaGS1BSrP8Rs",
                        "interval": "month",
                        "interval_count": 1,
                        "livemode": False,
                        "metadata": {},
                        "nickname": None,
                        "object": "plan",
                        "product": "prod_Nc4kjj2XYpywZV",
                        "tiers": None,
                        "tiers_mode": None,
                        "transform_usage": None,
                        "trial_period_days": None,
                        "usage_type": "licensed"
                    },
                    "quantity": 1,
                    "schedule": None,
                    "start_date": 1680064014,
                    "status": "active",
                    "tax_percent": None,
                    "test_clock": "clock_1Mqqb4Lt4dXK03v5NOFiPg4R",
                    "transfer_data": None,
                    "trial_end": 1680668814,
                    "trial_settings": {
                        "end_behavior": {
                            "missing_payment_method": "create_invoice"
                        }
                    },
                    "trial_start": 1680064014
                },
                "previous_attributes": {
                    "current_period_end": 1680668814,
                    "current_period_start": 1680064014,
                    "latest_invoice": "in_1Mqqb6Lt4dXK03v5Xn79tY8i",
                    "status": "trialing"
                }
            },
            "id": "evt_1MqqbKLt4dXK03v5qaIbiNCC",
            "livemode": False,
            "object": "event",
            "pending_webhooks": 1,
            "request": {
                "id": None,
                "idempotency_key": None
            },
            "type": "customer.subscription.updated"
        }
        get_event_from_webhook_mock.return_value = mock_response
        data = {
            "id": "evt_1MqqbKLt4dXK03v5qaIbiNCC",
            "object": "event",
            "api_version": "2023-08-16",
            "created": 1680064028,
            "type": "customer.subscription.updated",
            "data": {
                "object": {
                    "id": "sub_1Mqqb6Lt4dXK03v50OA219Ya",
                    "object": "subscription",
                    "application": None,
                    "application_fee_percent": None,
                    "automatic_tax": {
                        "enabled": False
                    },
                    "billing_cycle_anchor": 1680668814,
                    "billing_thresholds": None,
                    "cancel_at": None,
                    "cancel_at_period_end": False,
                    "canceled_at": None,
                    "cancellation_details": {
                        "comment": None,
                        "feedback": None,
                        "reason": None
                    },
                    "collection_method": "charge_automatically",
                    "created": 1680064014,
                    "currency": "usd",
                    "current_period_end": 1683260814,
                    "current_period_start": 1680668814,
                    "customer": "cus_M09xxkyq9tmgOu",
                    "days_until_due": None,
                    "default_payment_method": None,
                    "default_source": None,
                    "default_tax_rates": [],
                    "description": "A test subscription",
                    "discount": None,
                    "ended_at": None,
                    "invoice_customer_balance_settings": {
                        "consume_applied_balance_on_void": True
                    },
                    "items": {
                        "object": "list",
                        "data": [
                            {
                                "id": "si_Nc4kEcMHd3vRTS",
                                "object": "subscription_item",
                                "billing_thresholds": None,
                                "created": 1680064014,
                                "metadata": {},
                                "plan": {
                                    "id": "price_1IiiSnBZuKMpoaGS1BSrP8Rs",
                                    "object": "plan",
                                    "active": True,
                                    "aggregate_usage": None,
                                    "amount": 4242,
                                    "amount_decimal": "4242",
                                    "billing_scheme": "per_unit",
                                    "created": 1680064015,
                                    "currency": "usd",
                                    "interval": "month",
                                    "interval_count": 1,
                                    "livemode": False,
                                    "metadata": {},
                                    "nickname": None,
                                    "product": "prod_Nc4kjj2XYpywZV",
                                    "tiers": None,
                                    "tiers_mode": None,
                                    "transform_usage": None,
                                    "trial_period_days": None,
                                    "usage_type": "licensed"
                                },
                                "price": {
                                    "id": "price_1Mqqb5Lt4dXK03v5cK9prani",
                                    "object": "price",
                                    "active": True,
                                    "billing_scheme": "per_unit",
                                    "created": 1680064015,
                                    "currency": "usd",
                                    "custom_unit_amount": None,
                                    "livemode": False,
                                    "lookup_key": None,
                                    "metadata": {},
                                    "migrate_to": None,
                                    "nickname": None,
                                    "product": "prod_Nc4kjj2XYpywZV",
                                    "recurring": {
                                        "aggregate_usage": None,
                                        "interval": "month",
                                        "interval_count": 1,
                                        "trial_period_days": None,
                                        "usage_type": "licensed"
                                    },
                                    "tax_behavior": "unspecified",
                                    "tiers_mode": None,
                                    "transform_quantity": None,
                                    "type": "recurring",
                                    "unit_amount": 4242,
                                    "unit_amount_decimal": "4242"
                                },
                                "quantity": 1,
                                "subscription": "sub_1Mqqb6Lt4dXK03v50OA219Ya",
                                "tax_rates": []
                            }
                        ],
                        "has_more": False,
                        "total_count": 1,
                        "url": "/v1/subscription_items?subscription=sub_1Mqqb6Lt4dXK03v50OA219Ya"
                    },
                    "latest_invoice": "in_1MqqbILt4dXK03v5cbbciqFZ",
                    "livemode": False,
                    "plan": {
                        "id": "price_1IiiSnBZuKMpoaGS1BSrP8Rs",
                        "object": "plan",
                        "active": True,
                        "aggregate_usage": None,
                        "amount": 4242,
                        "amount_decimal": "4242",
                        "billing_scheme": "per_unit",
                        "created": 1680064015,
                        "currency": "usd",
                        "interval": "month",
                        "interval_count": 1,
                        "livemode": False,
                        "metadata": {},
                        "nickname": None,
                        "product": "prod_Nc4kjj2XYpywZV",
                        "tiers": None,
                        "tiers_mode": None,
                        "transform_usage": None,
                        "trial_period_days": None,
                        "usage_type": "licensed"
                    }
                },
                "previous_attributes": {
                    "current_period_end": 1680668814,
                    "current_period_start": 1680064014,
                    "latest_invoice": "in_1Mqqb6Lt4dXK03v5Xn79tY8i",
                    "status": "trialing"
                }
            }
        }
        url = '/modules/payments/stripe_webhook/'
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, '')

    @mock.patch(
        'modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.get_event_from_webhook')
    @mock.patch(
        'modules.payments.payments.services.stripe_subscription.StripeSubscriptionService.handle_webhook_events')
    def test_post_webhook_with_value_error(self, get_event_from_webhook_mock, handle_webhook_events_mock):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        def mock_get_event_from_webhook(payload):
            raise ValueError("Invalid payload")

        data = None
        get_event_from_webhook_mock.side_effect = mock_get_event_from_webhook
        url = '/modules/payments/stripe_webhook/'
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, ('Invalid payload',))
