from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, mixins
from uuid import uuid1

from .models import Quiz, QuizQuestion, QuizQuestionAnswer, AnonymousUserAnswer
from .serializers import (
    QuizSerializer,
    QuizUpdateSerializer,
    QuestionSerializer,
    AnswerSerializer,
    AllUserAnswerSerializer,
    TextAnswerSerializer,
    SingleChoiceSerializer,
    MultipleChoiceSerializer,
)


class QuizViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Quiz.objects.all()

    def get_serializer_class(self):
        if self.action == "update":
            return QuizUpdateSerializer
        else:
            return QuizSerializer


class QuizQuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        if self.action == "list":
            return QuizQuestion.objects.filter(quiz_id=self.kwargs["pk"])
        else:
            return QuizQuestion.objects.all()


class QuizQuestionAnswerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Quiz.objects.all()
    serializer_class = AnswerSerializer

    def get_queryset(self):
        if self.action == "list":
            return QuizQuestionAnswer.objects.filter(quiz_question_id=self.kwargs["pk"])
        else:
            return QuizQuestionAnswer.objects.all()


class CreateAnonymousUserAnswerView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = QuizQuestionAnswer.objects.all()

    def get_serializer_class(self):
        question = get_object_or_404(
            QuizQuestion,
            pk=self.kwargs["pk"],
        )
        if question.type == "TA":
            return TextAnswerSerializer
        elif question.type == "SC":
            return SingleChoiceSerializer
        elif question.type == "MC":
            return MultipleChoiceSerializer

    def perform_create(self, serializer):
        try:
            self.request.session["author_id"]
        except:
            self.request.session["author_id"] = int(str(uuid1().int)[:10])
        question = get_object_or_404(
            QuizQuestion,
            pk=self.kwargs["pk"],
        )
        quiz = Quiz.objects.get(pk=getattr(question, "quiz_id"))

        serializer.save(
            author=self.request.session["author_id"], question=question, quiz=quiz
        )


class AllUserAnswerView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AllUserAnswerSerializer

    def get_queryset(self):
        try:
            self.request.session["author_id"]
        except:
            self.request.session["author_id"] = int(str(uuid1().int)[:10])
        return AnonymousUserAnswer.objects.filter(
            author=int(self.request.session["author_id"])
        )
