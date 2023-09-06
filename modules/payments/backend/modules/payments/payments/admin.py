from django.contrib import admin

from .models import StripeSetting, StripeUserProfile, AppleIAPProduct, SubscriptionPlan, UserSubscription, \
    StripeWebhookLog, UserSubscriptionHistory

admin.site.register(StripeUserProfile)
admin.site.register(StripeSetting)
admin.site.register(AppleIAPProduct)


class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'interval', 'price', 'plan_type', 'is_active')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('interval', 'price', 'plan_type')


admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'tier', 'created_at')
    list_filter = ('created_at', 'updated_at')


admin.site.register(UserSubscription, UserSubscriptionAdmin)


class StripeWebhookLogAdmin(admin.ModelAdmin):
    list_display = ('type', 'data', 'created_at')
    list_filter = ('created_at', 'updated_at')


admin.site.register(StripeWebhookLog, StripeWebhookLogAdmin)


class UserSubscriptionHistoryAdmin(admin.ModelAdmin):
    list_display = ('sub', 'action', 'created_at')
    list_filter = ('created_at', 'updated_at')


admin.site.register(UserSubscriptionHistory, UserSubscriptionHistoryAdmin)
