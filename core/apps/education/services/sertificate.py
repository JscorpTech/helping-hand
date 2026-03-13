from pathlib import Path
from uuid import uuid4

from weasyprint import HTML
from django.conf import settings

from core.apps.accounts.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

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
        pdf_data = HTML(string=self.get_sertificate()).write_pdf()
        default_storage.save(file_name, ContentFile(pdf_data))
        return file_name
