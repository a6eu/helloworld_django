from django.db import models


from django.core import validators
from django.utils import timezone
from django.utils.functional import cached_property


class Question(models.Model):
    question_text = models.CharField(max_length=255)

    def str(self):
        return f"question text : {self.question_text} "





































