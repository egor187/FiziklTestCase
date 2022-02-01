from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from WeekDayResolver.serializers import WDResultSerializer, WDQuestionSerializer
from WeekDayResolver.core import WDResolver
from loguru import logger


from WeekDayResolver.exceptions import (
    LeapYearException,
    IncorrectDateISOFormatException,
    IncorrectRequestPayloadException,
)


class MainView(APIView):
    def post(self, request):
        try:
            date = WDQuestionSerializer(request.data).data
        except KeyError as e:
            logger.error(f"Incorrect passed key to serializer: {e}")
            return Response(
                {"msg": "Provide correct payload: {'date': YYYY-MM-DD}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            answer = WDResolver(date.get("date")).calculate()
        except LeapYearException:
            return Response(
                {"msg": "Nice try. Leap year has no Feb 29"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except IncorrectDateISOFormatException:
            return Response(
                {"msg": "Provide date in ISO format: YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = WDResultSerializer(answer)

        return Response(response.data, status=status.HTTP_200_OK)
