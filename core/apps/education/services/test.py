from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class TestService:

    def __init__(self): ...

    def calculate_score_and_balance(self, question, variants):
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

    def check_answer_validity(question, variants):
        # Tekshirish: Ko'p variantli savollar uchun cheklov
        if not question.is_many and len(variants) > 1:
            raise ValidationError({"variant": [_("Variantlar soni 1 ta bo'lishi kerak.")]})

        # Tekshirish: Variantlarning to'g'riligi
        variant_ids = [variant.id for variant in variants]
        if question.variants.filter(id__in=variant_ids).count() != len(variants):
            raise ValidationError({"variant": [_("Variantlar noto'g'ri tekshirilishi kerak.")]})

    def proccess_answers(self, answers) -> tuple:
        success = 0
        bal = 0

        for answer in answers:
            if "question" not in answer or "variant" not in answer:
                raise ValueError("Each answer must contain 'question' and 'variant' keys.")

            question = answer["question"]
            variants = answer["variant"]

            # calculate_score_and_balance natijasini bir marta chaqiramiz
            score, balance = self.calculate_score_and_balance(question, variants)

            success += score
            bal += balance

        return success, bal
