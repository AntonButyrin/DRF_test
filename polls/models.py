from django.db import models


class Poll(models.Model):
    """ Create Polls """
    name = models.CharField(max_length=64, db_index=True, verbose_name="Название опроса")
    description = models.TextField(max_length=1024, verbose_name="Описание опроса")
    start_poll = models.DateField(verbose_name="Дата старта")
    end_poll = models.DateField(verbose_name="Дата завершения опроса")

    def __str__(self):
        return self.name


class Question(models.Model):
    """ Create Questions """
    question_text = models.CharField(max_length=1024)
    question_type = models.CharField(max_length=1024)

    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """ Create Choice """
    choice_text = models.CharField(max_length=1024)

    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    """ Create Answer """
    choice_text = models.CharField(max_length=1024, null=True)
    user_id = models.IntegerField()

    poll = models.ForeignKey(Poll, related_name='poll', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name='choice', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.choice_text
