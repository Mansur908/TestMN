import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from api.helpers import send_to_kafka
from api.models import Message
from api.permissons.permission import ListenerOnly
from api.serializers import AddMessageSerializer, CheckMessageSerializer


class AddMessage(APIView):
    """
    post:Добавить сообщение
    """

    serializer_class = AddMessageSerializer

    def post(self, request):
        review = AddMessageSerializer(data=request.data)
        if review.is_valid() and int(request.data.get('user_id')) > 0:
            try:
                review.save()
            except KeyError:
                return Response({"error": "incorrect data"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "incorrect data"}, status=HTTP_400_BAD_REQUEST)
        try:
            # Отправка сообшения в Kafka
            send_to_kafka(review.instance.id, review.instance.message)
        except:
            return Response({"error": "error"}, status=HTTP_400_BAD_REQUEST)
        return Response("Successfully", status=HTTP_200_OK)


class CheckMessage(APIView):
    """
    post:Изменить статус сообщения
    """

    serializer_class = CheckMessageSerializer
    permission_classes = [ListenerOnly]

    def post(self, request):
        review = CheckMessageSerializer(data=request.data)
        try:
            if not Message.objects.filter(id=int(request.data.get("message_id"))):
                return Response({"error": "message with this id does not exist"}, status=HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "incorrect id"}, status=HTTP_400_BAD_REQUEST)
        if review.is_valid():
            try:
                if review.data.get("success"):
                    status = "correct"
                else:
                    status = "blocked"
                Message.objects.filter(id=review.data.get("message_id")).update(status=status)
            except KeyError:
                return Response({"error": "error adding to database"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "incorrect data"}, status=HTTP_400_BAD_REQUEST)
        return Response("Successfully", status=HTTP_200_OK)


class GetJwtToken(APIView):
    """
    post: Получить JWT токен
    """

    def post(self, request):
        if request.data.get('secret') == settings.SECRET_KEY:
            payload_data = {
                "role": "post_message_confirm"
            }
            token = jwt.encode(payload=payload_data, key=settings.SECRET_KEY)
            return Response({'token': token})
        else:
            payload_data = {
                "role": "none"
            }
            token = jwt.encode(payload=payload_data, key=settings.SECRET_KEY)
            return Response({'token': token})
