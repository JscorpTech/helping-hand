from modeltranslation.translator import TranslationOptions, register

from ..models import GuideModel


@register(GuideModel)
class GuideTranslation(TranslationOptions):
    fields = ["name", "desc", "file"]
