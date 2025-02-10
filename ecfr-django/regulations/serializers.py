from rest_framework import serializers
from .models import Agency, Title


class AgencyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ["name"]


class AgencyWordCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ["name", "cfr_word_count", "slug"]


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = [
            "number",
            "name",
            "latest_amended_on",
            "latest_issue_date",
            "up_to_date_as_of",
            "reserved",
        ]
