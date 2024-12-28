from rest_framework import serializers

from ...models import SertificateModel


class BaseSertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SertificateModel
        exclude = [
            "created_at",
            "updated_at",
        ]


class ListSertificateSerializer(BaseSertificateSerializer):
    class Meta(BaseSertificateSerializer.Meta): ...


class RetrieveSertificateSerializer(BaseSertificateSerializer):
    class Meta(BaseSertificateSerializer.Meta): ...


class CreateSertificateSerializer(BaseSertificateSerializer):
    class Meta(BaseSertificateSerializer.Meta): ...
