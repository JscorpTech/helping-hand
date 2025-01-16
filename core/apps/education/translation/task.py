from modeltranslation.translator import TranslationOptions, register

from ..models import TaskModel


@register(TaskModel)
class GuideTranslation(TranslationOptions):
    fields = [
        "name",
        "desc",
    ]
