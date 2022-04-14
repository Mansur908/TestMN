from rest_framework import serializers

from api.models import Message


class AddMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["user_id", "message"]

class CheckMessageSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    success = serializers.BooleanField()