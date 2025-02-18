from modeltranslation.translator import TranslationOptions, register

from ..models import FaqCategoryModel, FaqModel


@register(FaqCategoryModel)
class FaqCategoryTranslation(TranslationOptions):
    fields = [
        "name",
    ]


@register(FaqModel)
class FaqTranslation(TranslationOptions):
    fields = [
        "question",
        "answer",
    ]
