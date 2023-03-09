from rest_framework import serializers

from .models import Test


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'#('title', 'test2')

'''
Это подробный код, описываюший что под копотом ф_TestSerializer
class TestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    test2 = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return Test.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.test2 = validated_data.get('test2', instance.test2)
        instance.save()

        return instance
'''