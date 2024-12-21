from modeltranslation.translator import TranslationOptions, register

from ..models import QuestionModel, TestModel, VariantModel


@register(TestModel)
class TestTranslation(TranslationOptions):
    fields = []


@register(VariantModel)
class VariantTranslation(TranslationOptions):
    fields = []


@register(QuestionModel)
class QuestionTranslation(TranslationOptions):
    fields = []
