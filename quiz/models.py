from django.db import models
from django.utils import timezone as tz


class Quiz(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()
    start_date = models.DateTimeField(default=tz.now)
    end_date = models.DateTimeField()


class QuizQuestion(models.Model):
    QUIZ_QUESTION_TYPE_CHOICES = [
        ("TA", "Text answer"),
        ("SC", "Single choice"),
        ("MC", "Multiple choice"),
    ]
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE, related_name="questions")
    content = models.CharField(max_length=1000)
    type = models.CharField(
        max_length=2, choices=QUIZ_QUESTION_TYPE_CHOICES, default="TA"
    )


class QuizQuestionAnswer(models.Model):
    quiz_question = models.ForeignKey(
        "QuizQuestion", on_delete=models.CASCADE, related_name="answers"
    )
    content = models.CharField(max_length=1000)


class AnonymousUserAnswer(models.Model):
    author = models.IntegerField()
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE, related_name="user_quiz")
    question = models.ForeignKey(
        "QuizQuestion", on_delete=models.CASCADE, related_name="user_answers"
    )
    multiple_choice = models.ManyToManyField("QuizQuestionAnswer", blank=True)
    single_choice = models.ForeignKey(
        "QuizQuestionAnswer",
        on_delete=models.CASCADE,
        null=True,
        related_name="answers_one_choice",
    )
    text_answer = models.TextField(null=True)

    class Meta:
        unique_together = ("author", "question")
