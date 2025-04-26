from ..choices.tutorial import TutorialTypeChoice
from rest_framework.exceptions import ValidationError

def validate_tutorial_type(tutorial_type: str) -> bool:
    if tutorial_type not in [*TutorialTypeChoice.values, "all"]:
        raise ValidationError({
            "tutorial_type": "tutorial type not allowed"
        })