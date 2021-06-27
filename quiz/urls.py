from django.urls import path

from .views import *

urlpatterns = [
    path("quizzes/", QuizViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "quizzes/<int:pk>/",
        QuizViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "update", "delete": "destroy"}
        ),
    ),
    path(
        "quizzes/<int:pk>/questions/",
        QuizQuestionViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "question/<int:pk>/",
        QuizQuestionViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "update", "delete": "destroy"}
        ),
    ),
    path(
        "question/<int:pk>/answers/",
        QuizQuestionAnswerViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "answer/<int:pk>/",
        QuizQuestionAnswerViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "update", "delete": "destroy"}
        ),
    ),
    path(
        "question/<int:pk>/addanswer/",
        CreateAnonymousUserAnswerView.as_view({"post": "create"}),
    ),
    path("myanswers/", AllUserAnswerView.as_view({"get": "list"})),
]
