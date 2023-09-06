from unittest import mock

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import StripeUserProfile, StripeSetting, UserSubscription

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

    @mock.patch('modules.payments.payments.services.Stripe.stripe.Customer.create')
    @mock.patch('modules.payments.payments.services.Stripe.StripeService.create_payment_intent_sheet')
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

    @mock.patch('modules.payments.payments.services.Stripe.stripe.Customer.create')
    @mock.patch('modules.payments.payments.services.Stripe.StripeService.create_payment_intent_sheet')
    def test_create_payment_intent_with_stripe_setting(self, create_payment_intent_sheet_mock,
                                                       stripe_customer_create_mock):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.stripe_user_token.key)
        mock_response = dict(paymentIntent='pi_3MRXEOHocl234wo2ilpC0dsfde32me7kH_demo_2iOQZgcjjEs6I9rlRw73bK',
                             ephemeralKey='ek_test_demo3et637v5cvswfx36s62a2avg2ge67fwav2662z2',
                             customer='cus_demoos3dsd342ds23d')
        create_payment_intent_sheet_mock.return_value = mock_response
        stripe_customer_create_mock.return_value = {"id": "cus_demoos3dsd342ds23d"}
        url = '/modules/payments/create_payment_intent_sheet/'
        response = self.client.post(url, format='json')
        self.assertEqual(mock_response['paymentIntent'], response.data['paymentIntent'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        create_payment_intent_sheet_mock.assert_called_once()
        create_payment_intent_sheet_mock.assert_called_once_with(response.data['customer'], 100)

    @mock.patch('modules.payments.payments.services.Stripe.stripe.Customer.create')
    @mock.patch('modules.payments.payments.services.Stripe.StripeService.create_payment_intent_sheet')
    def test_create_payment_intent_with_stripe_setting_wallet_connect(self, create_payment_intent_sheet_mock,
                                                                      stripe_customer_create_mock):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.stripe_setting_user_token.key)
        mock_response = dict(paymentIntent='pi_demo degydge7823teg3db3ws_2iOQZgcjjEs6I9rlREMMw73bK',
                             ephemeralKey='ek_test_demo3et637v5cvswfx36s62a2avg2ge67fwav2662z2',
                             customer='cus_demoos3dsd342ds23d')
        create_payment_intent_sheet_mock.return_value = mock_response
        stripe_customer_create_mock.return_value = {"id": "cus_demoos3dsd342ds23d"}
        url = '/modules/payments/create_payment_intent_sheet/'
        response = self.client.post(url, format='json')
        self.assertEqual(mock_response['paymentIntent'], response.data['paymentIntent'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        create_payment_intent_sheet_mock.assert_called_once()

    @mock.patch('modules.payments.payments.services.Stripe.stripe.Customer.create')
    @mock.patch('modules.payments.payments.services.Stripe.StripeService.create_payment_intent_sheet')
    def test_create_payment_intent_with_stripe_customer_id(self, create_payment_intent_sheet_mock,
                                                           stripe_customer_create_mock):
        new_user = User.objects.create(username='wick', email='wick77@gmail.com', password='wick123@')
        tokens = Token.objects.create(user=new_user)
        stripe_profile, created = StripeUserProfile.objects.get_or_create(user_id=new_user.pk)
        if not created:
            stripe_profile.stripe_cus_id = "cus_demoos3dsd342ds23d"
            stripe_profile.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tokens.key)
        mock_response = {'paymentIntent': 'pi_demo degydge7823teg3db3ws_2iOQZgcjjEs6I9rlREMMw73bK',
                         'ephemeralKey': 'ek_test_demo3et637v5cvswfx36s62a2avg2ge67fwav2662z2',
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

    @mock.patch('modules.payments.payments.services.Stripe.StripeService.get_payments_history')
    def test_get_stripe_payments_history(self, get_stripe_payments_mock):
        mock_response = {
            "success": True,
            "data": [
                {
                    "id": "pi_3MRXEOHoclwoilpC0abme7kH",
                    "object": "payment_intent",
                    "amount": 100,
                    "amount_capturable": 0,
                    "amount_details": {
                        "tip": {}
                    },
                    "amount_received": 0,
                    "capture_method": "automatic",
                    "client_secret": "pi_demo degydge7823teg3db3ws_2iOQZgcjjEs6I9rlREMMw73bK",
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

    @mock.patch('modules.payments.payments.services.Stripe.StripeService.get_payments_history')
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
                    "id": "pi_3MRXEOHoclwoilpC0abme7kH",
                    "object": "payment_intent",
                    "amount": 100,
                    "amount_capturable": 0,
                    "amount_details": {
                        "tip": {}
                    },
                    "amount_received": 0,
                    "capture_method": "automatic",
                    "client_secret": "pi_demo degydge7823teg3db3ws_2iOQZgcjjEs6I9rlREMMw73bK",
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

    @mock.patch('modules.payments.payments.services.Stripe.StripeService.get_payments_history')
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

    @mock.patch('modules.payments.payments.services.Stripe.StripeService.get_payments_methods')
    def test_get_payments_methods(self, get_payments_methods_mock):
        mock_response = {'success': True, 'data': []}
        get_payments_methods_mock.return_value = mock_response
        url = '/modules/payments/get_payments_methods/'
        response = self.client.get(url)
        self.assertEqual(response.data['success'], mock_response['success'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        get_payments_methods_mock.assert_called_once()
        get_payments_methods_mock.assert_called_once_with(None)

    @mock.patch('modules.payments.payments.services.Stripe.StripeService.get_payments_methods')
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

    @mock.patch('modules.payments.payments.services.Stripe.StripeService.get_payments_methods')
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
    @mock.patch('modules.payments.payments.services.StripeSubscription.StripeSubscriptionService.already_has_a_plan')
    @mock.patch('modules.payments.payments.services.StripeSubscription.StripeSubscriptionService.get_price_details')
    @mock.patch('modules.payments.payments.services.StripeSubscription.StripeSubscriptionService.update_subscription')
    @mock.patch('modules.payments.payments.services.StripeSubscription.StripeSubscriptionService.create_subscription')
    @mock.patch('modules.payments.payments.services.Stripe.stripe.Customer.create')
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
            "customer": "cus_demoau63t6td",
            "default_payment_method": "pm_demo2as4dged33",
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
                        "subscription": "sub_sdemo3e7sgy2gs",
                        "tax_rates": []
                    }
                ],
                "total_count": 1,
                "url": "/v1/subscription_items?subscription=sub_1Nn3sKBZuKMpoaGSnx87G3ET"
            },
            "latest_invoice": "in_dsye3td3sgsssa",
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
    @mock.patch('modules.payments.payments.services.StripeSubscription.StripeSubscriptionService.already_has_a_plan')
    @mock.patch('modules.payments.payments.services.StripeSubscription.StripeSubscriptionService.get_price_details')
    @mock.patch('modules.payments.payments.services.StripeSubscription.StripeSubscriptionService.update_subscription')
    @mock.patch('modules.payments.payments.services.StripeSubscription.StripeSubscriptionService.create_subscription')
    @mock.patch('modules.payments.payments.services.Stripe.stripe.Customer.create')
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
            "customer": "cus_demoau63t6td",
            "default_payment_method": "pm_demo2as4dged33",
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
                        "subscription": "sub_sdemo3e7sgy2gs",
                        "tax_rates": []
                    }
                ],
                "total_count": 1,
                "url": "/v1/subscription_items?subscription=sub_1Nn3sKBZuKMpoaGSnx87G3ET"
            },
            "latest_invoice": "in_dsye3td3sgsssa",
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

    @mock.patch('modules.payments.payments.services.StripeSubscription.StripeSubscriptionService.already_has_a_plan')
    @mock.patch('modules.payments.payments.services.StripeSubscription.StripeSubscriptionService.cancel_subscription')
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
            "id": "sub_1Nn3sKBZuKMpoaGSnx87G3ET",
            "items": {
                "data": [
                    {
                        "billing_thresholds": None,
                        "created": 1693938080,
                        "id": "si_OaELJd0jFThpiZ",
                        "quantity": 1,
                        "subscription": "sub_demoBZuKMpoaGSnx87G3ET",
                        "tax_rates": []
                    }
                ],
                "total_count": 1,
                "url": "/v1/subscription_items?subscription=sub_1Nn3sKBZuKMpoaGSnx87G3ET"
            },
            "latest_invoice": "in_demoBZuKMpoaGSqlYpHWcQ",
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
