from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

MyUser = get_user_model()


def get_file_upload_file_name(instance, filename) -> str:
    return f'uploads/automata/{instance.user.id}/{now().timestamp()}.p2'


class Uploads(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    file = models.FileField(upload_to=get_file_upload_file_name)

    def __str__(self):
        return f"{self.name} - {self.user}"
