from __future__ import annotations

from api.v1.serializers import ImageSerializerVersion1, WorkSerializerVersion1


def get_serializer_classes(api_version: str) -> List[serializers]:
    api_serializer_mapping = {
        "v1": [WorkSerializerVersion1, ImageSerializerVersion1]
    }
    serializer_classes = api_serializer_mapping.get(api_version)
    return serializer_classes
