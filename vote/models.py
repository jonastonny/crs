from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.


class Room(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('owner', 'title')

    def get_absolute_url(self):
        return reverse('room_detail', kwargs={'pk': self.pk})

    def has_questiongroups(self):
        return len(self.questiongroup_set.all()) > 0

    def has_open_questiongroups(self):
        for questiongroup in self.questiongroup_set.all():
            if questiongroup.is_open:
                return True
        return False

    def total_subscribers(self):
        return len(self.subscription_set.all())

    def __str__(self):
        return self.title


class QuestionGroup(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_open = models.BooleanField(default=False)

    def has_questions(self):
        return len(self.question_set.all()) > 0

    def get_absolute_url(self):
        return reverse('questiongroup_detail', kwargs={'room': self.room_id, 'pk': self.pk})

    class Meta:
        unique_together = ('room', 'title')

    def __str__(self):
        return self.title


class Question(models.Model):
    group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE)
    question_text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    is_open = models.BooleanField(default=False)

    def percentages_correct(self):
        correct_responses = 0
        all_responses = 0
        has_correct_answer = False
        for answer in self.answer_set.all():
            count = answer.response_set.count()
            if answer.correct:
                has_correct_answer = True
                correct_responses += count
                all_responses += count
            else:
                all_responses += count
        if all_responses == 0:
            return has_correct_answer, 0.0
        else:
            return has_correct_answer, round(100 / all_responses * correct_responses, 1)

    def number_of_possible_answers(self):
        return self.answer_set.count()

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'room': self.group.room.id,
                                                  'questiongroup': self.group.id,
                                                  'pk': self.id})

    def total_responses(self):
        total_sum = 0
        for answer in self.answer_set.all():
            total_sum += answer.number_of_responses()
        return total_sum

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    correct = models.BooleanField(default=False)

    def number_of_responses(self):
        return self.response_set.count()

    def __str__(self):
        return self.answer_text


class Response(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'question',)

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

