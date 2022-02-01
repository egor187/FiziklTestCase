from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from WeekDayResolver.serializers import WDResultSerializer, WDQuestionSerializer
from WeekDayResolver.core import WDResolver
from loguru import logger


class MainView(APIView):

    def post(self, request):
        try:
            date = WDQuestionSerializer(request.data).data
        except KeyError as e:
            logger.error(f"Incorrect passed key to serializer: {e}")
            return Response({"msg": "Provide correct payload: {'date': YYYY-MM-DD}"}, status=status.HTTP_400_BAD_REQUEST)

        answer = WDResolver(date.get("date")).calculate()
        if not answer:
            return Response({"msg": "Provide date in ISO format: YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        response = WDResultSerializer(answer)

        return Response(response.data, status=status.HTTP_200_OK)
