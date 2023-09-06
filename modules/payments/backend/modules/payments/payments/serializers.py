from rest_framework import serializers

from .models import StripeSetting, AppleIAPProduct, SubscriptionPlan


class StripeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeSetting
        fields = '__all__'


class AppleIAPSerializer(serializers.Serializer):
    productId = serializers.CharField()
    transactionDate = serializers.CharField()
    transactionId = serializers.CharField()
    transactionReceipt = serializers.CharField()
    user = serializers.SerializerMethodField(required=False)

    def get_user(self, obj):
        pass


class AppleIAPProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppleIAPProduct
        fields = '__all__'


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get("user")
        has_user_sub = hasattr(user, 'user_subscription')
        return user.user_subscription.tier == obj if has_user_sub else False

    class Meta:
        model = SubscriptionPlan
        fields = ["id", "name", "description", "price_id", "price", "interval", "is_subscribed"]
