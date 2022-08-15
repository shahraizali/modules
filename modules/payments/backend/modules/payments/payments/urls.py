from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import PaymentSheetView, GetStripePaymentsView, GetPaymentMethodsView, AppleIAPayment,\
    AppleIAProductsView


router = DefaultRouter()
router.register("apple/verify/receipt", AppleIAPayment, basename="apple-in-app")

urlpatterns = [
    path('apple/get_products/', AppleIAProductsView.as_view()),
    path('payment_sheet/', PaymentSheetView.as_view()),
    path('get_payments_history/', GetStripePaymentsView.as_view()),
    path('get_payments_methods/', GetPaymentMethodsView.as_view()),
    path("", include(router.urls)),
]