from modeltranslation.translator import TranslationOptions, register

from ..models import NotificationModel


@register(NotificationModel)
class NotificationTranslation(TranslationOptions):
    fields = [
        "title",
        "body",
    ]
