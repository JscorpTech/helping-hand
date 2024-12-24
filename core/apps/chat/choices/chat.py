from django.db import models
from django.utils.translation import gettext_lazy as _


class ChatTypeChoice(models.TextChoices):
    LAWYER = "lawyer", _("Lawyer")
    PSIXOLOG = "psixolog", _("Psixolog")


class FileTypeChoice(models.TextChoices):
    IMAGE = "image", _("Image")
    FILE = "file", _("File")
    VIDEO = "video", _("Video")
    AUDIO = "audio", _("Audio")
    TEXT = "text", _("Text")
    OTHER = "other", _("Other")
