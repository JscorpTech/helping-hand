from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    moderators_count=serializers.IntegerField()
    news_count=serializers.IntegerField()
    sertificated_users_count=serializers.IntegerField()
    users_count=serializers.IntegerField()
    videos_count=serializers.IntegerField()
    endangered_users_count=serializers.IntegerField()

