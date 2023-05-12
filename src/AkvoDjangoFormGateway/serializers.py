from collections import OrderedDict
from rest_framework import serializers
from .models import (
    AkvoGatewayForm,
    AkvoGatewayQuestion,
    AkvoGatewayQuestionOption,
    AkvoGatewayData,
    AkvoGatewayAnswer,
)
from .constants import QuestionTypes
from .utils.functions import get_answer_value


class ListFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = AkvoGatewayForm
        fields = ['id', 'name', 'description', 'version']


class ListOptionSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super(ListOptionSerializer, self).to_representation(instance)
        return OrderedDict(
            [(key, result[key]) for key in result if result[key] is not None]
        )

    class Meta:
        model = AkvoGatewayQuestionOption
        fields = ['id', 'name', 'order']


class ListQuestionSerializer(serializers.ModelSerializer):
    option = serializers.SerializerMethodField()

    class Meta:
        model = AkvoGatewayForm
        fields = ['id', 'name', 'description', 'version']

    def get_option(self, instance: AkvoGatewayQuestion):
        if instance.type in [
            QuestionTypes.option,
            QuestionTypes.multiple_option,
        ]:
            return ListOptionSerializer(
                instance=instance.ag_question_question_options.all(), many=True
            ).data
        return None


class ListDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AkvoGatewayData
        fields = ['id', 'name', 'form', 'geo', 'phone', 'created', 'updated']


class ListDataAnswerSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = AkvoGatewayAnswer
        fields = ['history', 'question', 'value']

    def get_value(self, instance: AkvoGatewayAnswer):
        return get_answer_value(instance)
