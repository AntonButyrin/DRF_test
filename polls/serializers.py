from rest_framework import serializers

from .models import Poll, Question, Choice, Answer


class ChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    choice_text = serializers.CharField(max_length=200)

    def validate(self, attrs):
        try:
            obj = Choice.objects.get(question=attrs['question'].id, choice_text=attrs['choice_text'])
        except Choice.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('Выбор уже существует')

    class Meta:
        model = Choice
        fields = '__all__'

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    poll = serializers.SlugRelatedField(queryset=Poll.objects.all(), slug_field='id')
    question_text = serializers.CharField(max_length=200)
    question_type = serializers.CharField(max_length=200)
    choices = ChoiceSerializer(many=True, read_only=True)

    def validate(self, attrs):
        question_type = attrs['question_type']
        if question_type == 'one' or question_type == 'multiple' or question_type == 'text':
            return attrs
        raise serializers.ValidationError('Тип вопроса может быть только один, несколько или текстовый')

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class PollSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    poll_name = serializers.CharField(max_length=200)
    pub_date = serializers.DateField()
    end_date = serializers.DateField()
    poll_description = serializers.CharField(max_length=200)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'pub_date' in validated_data:
            raise serializers.ValidationError({'pub_date': 'Вы не можете изменять это поле.'})
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class CurrentUserDefault(object):
    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id

    def __call__(self):
        return self.user_id


class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(default=CurrentUserDefault())
    poll = serializers.SlugRelatedField(queryset=Poll.objects.all(), slug_field='id')
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    choice = serializers.SlugRelatedField(queryset=Choice.objects.all(), slug_field='id', allow_null=True)
    choice_text = serializers.CharField(max_length=200, allow_null=True, required=False)

    class Meta:
        model = Answer
        fields = '__all__'

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def validate(self, attrs):
        question_type = Question.objects.get(id=attrs['question'].id).question_type
        try:
            if question_type == "one" or question_type == "text":
                obj = Answer.objects.get(question=attrs['question'].id, survey=attrs['poll'],
                                         user_id=attrs['user_id'])
            elif question_type == "multiple":
                obj = Answer.objects.get(question=attrs['question'].id, survey=attrs['poll'],
                                         user_id=attrs['user_id'],
                                         choice=attrs['choice'])
        except Answer.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('Уже ответил')