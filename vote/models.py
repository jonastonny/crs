from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Room(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=1000)
    date_time = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField('date published')

    def number_of_possible_answers(self):
        return self.answer_set.count()


    #def number_of_responses:

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #choices = models.ManyToManyField(User, through='Choice')
    answer_text = models.CharField(max_length=500)
    date_time = models.DateField()

    def __str__(self):
        return self.answer_text


class Choice(models.Model):
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)
    date_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s @ %s" % (self.user.username, self.answer.answer_text)



