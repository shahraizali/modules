from django.urls import re_path, path, include
from rest_framework.routers import DefaultRouter

from .viewsets import PaymentSheetView, GetStripePaymentsView, GetPaymentMethodsView, AppleIAProductsView, \
    AppleIAPayment, SubscriptionPlanView, BuySubscriptionPlanView, CancelSubscriptionPlanView, StripeWebhookView

router = DefaultRouter()
router.register("apple/verify/receipt", AppleIAPayment, basename="apple-in-app")

urlpatterns = [
    re_path('apple/get_products/?', AppleIAProductsView.as_view()),
    re_path(r'create_payment_intent_sheet/?', PaymentSheetView.as_view()),
    re_path(r'get_payments_history/?', GetStripePaymentsView.as_view()),
    re_path(r'get_payments_methods/?', GetPaymentMethodsView.as_view()),
    re_path(r'get_subscription_plans/?', SubscriptionPlanView.as_view()),
    re_path(r'buy_subscription_plan/?', BuySubscriptionPlanView.as_view()),
    re_path(r'cancel_subscription_plan/?', CancelSubscriptionPlanView.as_view()),
    re_path(r'stripe_webhook/?', StripeWebhookView.as_view()),
    path("", include(router.urls)),
]
