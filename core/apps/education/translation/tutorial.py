from modeltranslation.translator import TranslationOptions, register

from ..models import TutorialModel


@register(TutorialModel)
class TutorialTranslation(TranslationOptions):
    fields = [
        "name",
        "desc",
    ]
