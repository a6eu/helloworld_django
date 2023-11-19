from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return f"question text : {self.question_text} "


