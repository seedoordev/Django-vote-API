from collections import OrderedDict

from rest_framework import serializers

from .models import Quiz, QuizQuestion, QuizQuestionAnswer, AnonymousUserAnswer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestionAnswer
        fields = "__all__"

    def validate(self, data):
        if getattr(data["quiz_question"], "type") == "TA":
            raise serializers.ValidationError(
                "Нельзя добавить ответ для такого типа вопроса"
            )
        return data


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = "__all__"

    def to_representation(self, instance):
        result = super(QuestionSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key]])


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = "__all__"

    def validate(self, data):
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError(
                "Опрос должен начинаться раньше чем заканчивается"
            )
        return data

    def to_representation(self, instance):
        result = super(QuizSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key]])


class QuizUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        exclude = ("start_date",)

    def validate(self, data):
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError(
                "Опрос должен начинаться раньше чем заканчивается"
            )
        return data


class AllUserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousUserAnswer
        fields = "__all__"

    def to_representation(self, instance):
        result = super(AllUserAnswerSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key]])


class TextAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousUserAnswer
        fields = ("text_answer",)

    def validate(self, data):
        if not data["text_answer"]:
            raise serializers.ValidationError("Укажите Ваш ответ")
        return data


class SingleChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousUserAnswer
        fields = ("single_choice",)

    def validate(self, data):
        if not data["single_choice"]:
            raise serializers.ValidationError("Укажите Ваш ответ")
        return data


class MultipleChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousUserAnswer
        fields = ("multiple_choice",)

    def validate(self, data):
        if not data["multiple_choice"]:
            raise serializers.ValidationError("Укажите Ваш ответ")
        return data
