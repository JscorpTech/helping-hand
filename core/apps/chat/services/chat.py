from core.apps.chat.serializers import ListUserSerializer


class ChatService:

    def __init__(self, context={}):
        self.context = context

    def call(self, data):
        return {
            "connection_id": data["data"]["connection_id"],
            "group_id": data["group"],
            "user": ListUserSerializer(self.context["user"]).data,
        }

    def action(self, data):
        match data["action"]:
            case "call":
                return self.call(data)
            case _:
                return {}

    def process(self, data) -> dict:
        response = self.action(data)
        return {
            "group": "group_%s" % data["group"],
            "data": response,
        }
