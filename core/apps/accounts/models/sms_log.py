import math

from django.db import models


class SmsLog(models.Model):
    phone = models.CharField(max_length=20)
    message = models.TextField()
    sms_count = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=20, default="sent")
    error = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sms_log"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.phone} — {self.created_at:%Y-%m-%d %H:%M}"

    @staticmethod
    def calc_sms_count(text: str) -> int:
        length = len(text)
        if length <= 160:
            return 1
        return math.ceil(length / 153)

    @classmethod
    def log(cls, phone: str, message: str, status: str = "sent", error: str = "") -> "SmsLog":
        return cls.objects.create(
            phone=phone,
            message=message,
            sms_count=cls.calc_sms_count(message),
            status=status,
            error=error,
        )
