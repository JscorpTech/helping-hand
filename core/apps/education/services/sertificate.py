from pathlib import Path
from uuid import uuid4

import pdfkit
from django.conf import settings

from core.apps.accounts.models import User

from ..models import SertificateModel


class SertificateService:

    def __init__(self, user: User):
        self.user = user
        self.sertificate_template = settings.BASE_DIR / "resources/assets/sertificate.html"

    def create(self) -> SertificateModel:
        return SertificateModel.objects.create(user=self.user, file=self.generate())

    def get_sertificate(self) -> str:
        with open(self.sertificate_template, "r") as file:
            sertificate = file.read()
        return sertificate.replace("{{full_name}}", self.user.full_name)

    def generate(self) -> str:
        file_name = "sertificates/sertificate_%s.pdf" % uuid4()
        pdfkit.from_string(self.get_sertificate(), str(Path(settings.BASE_DIR, "resources/media/%s" % file_name)))
        return file_name
