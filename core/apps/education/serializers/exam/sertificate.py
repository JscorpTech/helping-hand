from rest_framework import serializers

from core.apps.accounts.serializers import UserSerializer

from ...models import SertificateModel


class BaseSertificateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SertificateModel
        exclude = [
            "created_at",
            "updated_at",
            "exam",
        ]


class ListMeSertificateSerializer(BaseSertificateSerializer):
    class Meta(BaseSertificateSerializer.Meta):
        exclude = None
        fields = ["id", "status", "file"]


class ListSertificateSerializer(BaseSertificateSerializer):
    class Meta(BaseSertificateSerializer.Meta): ...


class RetrieveSertificateSerializer(BaseSertificateSerializer):
    class Meta(BaseSertificateSerializer.Meta): ...


class CreateSertificateSerializer(BaseSertificateSerializer):
    class Meta(BaseSertificateSerializer.Meta): ...
