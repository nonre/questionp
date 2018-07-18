import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from polls.models import Question, Choice

class QuestionMethodTests(TestCase):
    def test_published_recently_with_future_question(self):
        time=timezone.now() + datetime.timedelta(days=90)
        future_question = Question(pub_date = time)
        self.assertEqual(future_question.published_recently(), False)

    def test_published_recently_with_old_question(self):
        time=timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.published_recently(),False)

    def test_published_recently_with_recent_question(self):
        time=timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.published_recently(),True)

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_with_no_questions(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'no polls are available')
        self.assertQuerysetEqual(response.context ['latest_questions'],[])

    def test_index_with_a_past_question(self):
        past_question=create_question(question_text ='Past question.',days = -30)
        past_question.choice_set.create(choice_text='A choice', votes=0)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context ['latest_questions'], ['<Question: Past question.>'])

    def test_index_with_a_future_question(self):
        create_question(question_text ='Future question.',days = 30)
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'no polls are available', status_code=200)
        self.assertQuerysetEqual(response.context ['latest_questions'],[])

    def test_index_with_past_question_and_future_question(self):
        past_question=create_question(question_text ='Past question.',days =-30)
        future_question=create_question(question_text ='Future question.',days = 30)
        past_question.choice_set.create(choice_text='A choice', votes=0)
        future_question.choice_set.create(choice_text='A choice', votes=0)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context['latest_questions'],['<Question: Past question.>'])

    def test_index_with_two_past_questions(self):
        past_question_1 = create_question(question_text ='Past question 1.',days =-30)
        past_question_2= create_question(question_text ='Past question 2.',days =-5)
        past_question_1.choice_set.create(choice_text='A choice', votes=0)
        past_question_2.choice_set.create(choice_text='A choice', votes=0)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context['latest_questions'],['<Question: Past question 2.>','<Question: Past question 1.>'])

class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        future_question = create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('detail',args =(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_future_question_past_question(self):
        past_question=create_question(question_text='Past question.', days=-30)
        response = self.client.get(reverse('detail',args=(past_question.id,)))
        self.assertContains(response,
        past_question.question_text, status_code=200)

class QuestionChoiceTests(TestCase):
    def test_question_with_no_choice(self):
        empty_question=create_question(question_text ='Empty question.',days = -1)
        full_question= create_question(question_text ='Full question. ',days = -1)
        full_question.choice_set.create(choice_text='This is the choice', votes=0)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context ['latest_questions'], ['<Question: Full question. >'])
