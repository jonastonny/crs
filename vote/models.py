from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.


class Room(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'title')

    def get_absolute_url(self):
        return reverse('room_detail', kwargs={'pk': self.pk})

    def has_questiongroups(self):
        return len(self.questiongroup_set.all()) > 0

    def __str__(self):
        return self.title


class QuestionGroup(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)
    # pub_date = models.DateTimeField('date published')
    is_open = models.BooleanField(default=False)

    def has_questions(self):
        return len(self.question_set.all()) > 0

    def get_absolute_url(self):
        return reverse('questiongroup_detail', kwargs={'room': self.room_id,'pk': self.pk})

    class Meta:
        unique_together = ('room', 'title')

    def __str__(self):
        return self.title


class Question(models.Model):
    group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=1000)
    date_time = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField('date published')
    is_open = models.BooleanField(default=False)

    def number_of_possible_answers(self):
        return self.answer_set.count()

    def total_responses(self):
        total_sum = 0
        for answer in self.answer_set.all():
            total_sum += answer.number_of_responses()
        return total_sum

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=500)
    date_time = models.DateTimeField(auto_now_add=True)

    def number_of_responses(self):
        return self.response_set.count()

    def __str__(self):
        return self.answer_text


class Response(models.Model):
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer',)

    def __str__(self):
        return "%s @ %s" % (self.user.username, self.answer.answer_text)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'room',)

    def __str__(self):
        return "%s subscribes to %s" % (self.user.username, self.room)

