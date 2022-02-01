from rest_framework import serializers


class WDResultSerializer(serializers.Serializer):
    week_number = serializers.IntegerField()


class WDQuestionSerializer(serializers.Serializer):
    date = serializers.CharField()
