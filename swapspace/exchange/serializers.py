from rest_framework import serializers
from exchange.models import Category

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'
		