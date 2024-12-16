from ..models import GroupModel, MessageModel
from faker import Faker


class ChatSeeder:

    def run(self):
        faker = Faker()
        for i in range(10):
            group = GroupModel.objects.create(name=faker.word())
            for i in range(100):
                MessageModel.objects.create(text=faker.word(), group=group, user_id=1)
