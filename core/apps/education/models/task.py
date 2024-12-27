from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from django.contrib.auth import get_user_model


class TaskModel(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255)
    desc = models.TextField(_("description"), blank=True, null=True)
    image = models.ImageField(_("banner"), upload_to="tasks/")
    file = models.FileField(_("file"), upload_to="tasks/", blank=True, null=True)
    is_file_answer = models.BooleanField(_("is answer file"), default=False)

    def __str__(self):
        return self.name

    @classmethod
    def _create_face(self):
        return self.objects.create(
            name="Test Task",
            desc="Test task for testing",
            image="image.jpg",
        )

    class Meta:
        db_table = "task"
        verbose_name = _("TaskModel")
        verbose_name_plural = _("TaskModels")


class TaskResultModel(AbstractBaseModel):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="taskresults",
    )
    task = models.ForeignKey("TaskModel", verbose_name=_("task"), on_delete=models.CASCADE, related_name="taskresults")
    tutorial = models.ForeignKey(
        "TutorialModel", verbose_name=_("tutorial"), on_delete=models.CASCADE, related_name="taskresults"
    )
    answer = models.TextField(_("answer"), blank=True, null=True)
    file = models.FileField(_("file"), upload_to="taskresults/", blank=True, null=True)

    def __str__(self):
        return self.task.name

    @classmethod
    def _create_face(self):
        return self.objects.create(
            user=get_user_model()._create_fake(),
            task=TaskModel._create_face(),
        )

    class Meta:
        db_table = "taskresult"
        verbose_name = _("TaskresultModel")
        verbose_name_plural = _("TaskresultModels")
