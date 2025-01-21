from rest_framework import serializers

from ...models import FaqModel


class BaseFaqSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "question", 
            "answer", 
            "updated_date",
            "created_date"
            ]



class ListFaqSerializer(BaseFaqSerializer):
    class Meta(BaseFaqSerializer.Meta):...

class RetreiveFaqSerializer(BaseFaqSerializer):
    class Meta(BaseFaqSerializer.Meta):...
    
class CreateFaqSerializer(BaseFaqSerializer):
    class Meta(BaseFaqSerializer.Meta):...
    