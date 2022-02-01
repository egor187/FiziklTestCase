from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from WeekDayResolver.serializers import WDResultSerializer, WDQuestionSerializer
from WeekDayResolver.core import WDResolver
from loguru import logger


class MainView(APIView):

    def post(self, request):
        serializer = WDQuestionSerializer(request.data)
        date = serializer.data
        answer = WDResolver(date.get("date")).calculate()
        if not answer:
            return Response({"msg": "Provide date in ISO format: YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        response = WDResultSerializer(answer)

        return Response(response.data, status=status.HTTP_200_OK)
