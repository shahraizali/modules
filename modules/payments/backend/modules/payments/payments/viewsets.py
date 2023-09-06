import os

from rest_framework import authentication, permissions, status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import StripeSetting, AppleIAPProduct, SubscriptionPlan
from .serializers import StripeSettingSerializer, AppleIAPProductSerializer, AppleIAPSerializer, \
    SubscriptionPlanSerializer
from .services.ApplePayment import ApplePaymentService
from .services.Stripe import StripeService
from .services.StripeSubscription import StripeSubscriptionService


class PaymentSheetView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Creates paymentIntent and Ephemeral key for the customer. If no customer exists, first creates one.
        Deduct and send the application fee to the Stripe connect account for 'Stripe Setting' users.
        body_params: "cents"
        """
        try:
            user = self.request.user
            stripe_profile = user.stripe_profile
            if not stripe_profile.stripe_cus_id:
                customer = StripeService.create_user(user=user)
                stripe_cus_id = customer['id']
                stripe_profile.stripe_cus_id = stripe_cus_id
                stripe_profile.save()
            else:
                stripe_cus_id = stripe_profile.stripe_cus_id

            cents = request.data.get('cents', 100)
            try:
                query = StripeSetting.objects.get(user=user)
                serializer = StripeSettingSerializer(query)
                if serializer.data['is_wallet_connect']:
                    response = StripeService.create_payment_intent_sheet(stripe_cus_id, cents,
                                                                         serializer.data['application_fee'],
                                                                         os.getenv("CONNECTED_STRIPE_ACCOUNT_ID"))
                else:
                    response = StripeService.create_payment_intent_sheet(stripe_cus_id, cents)
            except:
                response = StripeService.create_payment_intent_sheet(stripe_cus_id, cents)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


class GetStripePaymentsView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Returns array of PaymentIntents history for a stripe customer.
        """
        try:
            user = self.request.user
            stripe_profile = user.stripe_profile
            if not stripe_profile.stripe_cus_id:
                stripe_cus_id = None
            else:
                stripe_cus_id = stripe_profile.stripe_cus_id
            history = StripeService.get_payments_history(stripe_cus_id)
            response = {
                "success": True,
                "data": history
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


class GetPaymentMethodsView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Returns a list of PaymentMethods attached to the customer's StripeAccount.
        """
        try:
            user = self.request.user
            stripe_profile = user.stripe_profile
            if not stripe_profile.stripe_cus_id:
                stripe_cus_id = None
            else:
                stripe_cus_id = stripe_profile.stripe_cus_id
            history = StripeService.get_payments_methods(stripe_cus_id)
            response = {
                "success": True,
                "data": history
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionPlanView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Returns all the active subscription plans.
        :param request: Object containing user data.
        """
        plans = SubscriptionPlan.objects.filter(is_active=True)
        response = SubscriptionPlanSerializer(plans, many=True, context={'user': self.request.user})
        return Response({
            'success': True,
            'result': response.data,
        }, status=status.HTTP_200_OK)


class BuySubscriptionPlanView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Updates the existing subscription if there is one. Creates a new subscription otherwise.

        :param request: Object containing user data.
        """
        user = self.request.user
        stripe_profile = user.stripe_profile
        if not stripe_profile.stripe_cus_id:
            customer = StripeService.create_user(user=user)
            stripe_cus_id = customer['id']
            stripe_profile.stripe_cus_id = stripe_cus_id
            stripe_profile.save()
        else:
            stripe_cus_id = stripe_profile.stripe_cus_id
        price_tier = request.data.get('price_tier')
        plan = SubscriptionPlan.objects.get(price_id=price_tier)
        already_has_a_plan = StripeSubscriptionService.already_has_a_plan(user)
        if already_has_a_plan and already_has_a_plan.subscription_id:
            # update subscription
            result = StripeSubscriptionService.update_subscription(already_has_a_plan.subscription_id, plan.price_id)
        else:
            result = StripeSubscriptionService.create_subscription(stripe_cus_id, plan.price_id)
        response = result
        return Response(response, status=status.HTTP_200_OK)


class CancelSubscriptionPlanView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Cancels an existing subscription.

        :param request: Object containing existing user data.
        """
        user = self.request.user
        already_has_a_plan = StripeSubscriptionService.already_has_a_plan(user)
        deletedSubscription = StripeSubscriptionService.cancel_subscription(already_has_a_plan.subscription_id)
        already_has_a_plan.tier = None
        already_has_a_plan.subscription_id = ""
        already_has_a_plan.is_active = False
        already_has_a_plan.save()
        return Response("", status=status.HTTP_200_OK)


class StripeWebhookView(APIView):

    def post(self, request, *args, **kwargs):
        """
        Handles EVENTS created by the stripe.
        :param request: Event details by stripe
        """
        payload = self.request.body
        # sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        try:
            event = StripeSubscriptionService.get_event_from_webhook(payload)
            # TODO: Handle EVENTS and make user super or change subscription type
            StripeSubscriptionService.handle_webhook_events(event)
        except ValueError as e:
            # Invalid payload
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)

        return Response("", status=status.HTTP_200_OK)


class AppleIAProductsView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    queryset = AppleIAPProduct.objects.filter(is_active=True)
    serializer_class = AppleIAPProductSerializer


class AppleIAPayment(ViewSet):
    serializer_class = AppleIAPSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        """
        Verify an Apple receipt.
        """
        serializer = self.serializer_class(data=request.data)
        data = None
        if serializer.is_valid(raise_exception=True):
            verify_receipt, success = ApplePaymentService.verify_apple_receipt(request.data)
            print('verify_receipt', verify_receipt)
            if success:
                data = "success"
            else:
                data = "fail"
        return Response({
            'success': True,
            'result': data,
        }, status=status.HTTP_200_OK)
