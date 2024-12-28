from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class TestService:

    def __init__(self): ...

    @staticmethod
    def calculate_score_and_balance(question, variants):
        success = 0
        bal = 0

        # To'g'ri javoblarni tekshirish
        correct_count = question.variants.filter(is_true=True).count()
        selected_correct = sum(1 for variant in variants if variant.is_true)

        if correct_count == selected_correct:
            success += 1
        for variant in variants:
            if variant.is_true:
                bal += variant.bal

        return success, bal

    @staticmethod
    def check_answer_validity(question, variants):
        # Tekshirish: Ko'p variantli savollar uchun cheklov
        if not question.is_many and len(variants) > 1:
            raise ValidationError({"variant": [_("Variantlar soni 1 ta bo'lishi kerak.")]})

        # Tekshirish: Variantlarning to'g'riligi
        variant_ids = [variant.id for variant in variants]
        if question.variants.filter(id__in=variant_ids).count() != len(variants):
            raise ValidationError({"variant": [_("Variantlar noto'g'ri tekshirilishi kerak.")]})
