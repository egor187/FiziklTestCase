from rest_framework.test import APITestCase, RequestsClient
from rest_framework import status
from loguru import logger

logger.disable("WeekDayResolver.views")
logger.disable("WeekDayResolver.core")


class MainViewTest(APITestCase):

    url = "/weekday-resolver/"
    incorrect_payload = {"data": "1996-02-29"}
    incorrect_date_isoformat = {"data": "999-02-1"}
    incorrect_leap_year_date = {"date": "1997-02-29"}
    incorrect_payload_msg = {"msg": "Provide correct payload: {'date': YYYY-MM-DD}"}
    incorrect_leap_year_date_msg = {'msg': 'Nice try. Leap year has no Feb 29'}
    correct_payload = {"date": "2019-01-05"}
    correct_msg = {'week_number': 1}

    def test_payload_format(self):
        incorrect_payload_response = self.client.post(self.url, self.incorrect_payload, format="json")
        self.assertEqual(incorrect_payload_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(incorrect_payload_response.json(), self.incorrect_payload_msg)

        incorrect_date_isoformat_response = self.client.post(self.url, self.incorrect_date_isoformat, format="json")
        self.assertEqual(incorrect_date_isoformat_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(incorrect_date_isoformat_response.json(), self.incorrect_payload_msg)

    def test_leap_year(self):
        response = self.client.post(self.url, self.incorrect_leap_year_date, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), self.incorrect_leap_year_date_msg)

    def test_correct_output(self):
        response = self.client.post(self.url, self.correct_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), self.correct_msg)

    def test_outdoor_request(self):
        client = RequestsClient()
        response = client.post("http://localhost:8000/weekday-resolver/", json=self.correct_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("week_number"), 1)
