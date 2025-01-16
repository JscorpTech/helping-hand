from modeltranslation.translator import TranslationOptions, register

from ..models import QuestionModel, TestModel, VariantModel


@register(TestModel)
class TestTranslation(TranslationOptions):
    fields = [
        "topic",
        "desc",
    ]


@register(VariantModel)
class VariantTranslation(TranslationOptions):
    fields = [
        "variant"
    ]


@register(QuestionModel)
class QuestionTranslation(TranslationOptions):
    fields = [
        "question"
    ]
