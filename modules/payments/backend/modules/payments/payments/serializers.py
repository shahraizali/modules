from rest_framework import serializers
from payments.models import AppleIAPProduct

class appleIAPSerializer(serializers.Serializer):
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