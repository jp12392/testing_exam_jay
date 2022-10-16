from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model

from accounts.models import Question, QuestionOptions, QuestionSet
User = get_user_model()


### QuestionOptions Serializer.
class QuestionOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOptions
        fields = ['id','question','text','image','order']

### Question Serialziter
class QuestionSerializer(serializers.ModelSerializer):
    question_option_list = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ['id','question_set','text','image','type','order','marks','question_option_list']

    def get_question_option_list(self, obj):
        qs_option = QuestionOptions.objects.filter(question_id=obj.id).all()
        serializer_opt = QuestionOptionsSerializer(qs_option, many=True)
        return serializer_opt.data


## Question Set Serializer.
class QuestionSetSerializer(serializers.ModelSerializer):
    question_list = serializers.SerializerMethodField()
    class Meta:
        model = QuestionSet
        fields = ['id','name','slug','enable_negative_marking','negative_marking_percentage','ideal_timeto_complete','question_list']

    def get_question_list(self, obj):
        question = Question.objects.filter(question_set_id=obj.id).all()
        serializer_qs = QuestionSerializer(question, many=True)
        return serializer_qs.data