from rest_framework import serializers

from works.models import Work


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = [
            "id",
            "title",
            "year_from",
            "year_to",
            "technique",
            "height",
            "width",
            "depth",
            "description",
        ]
