from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from polls.models import Question, Choice
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.utils import timezone

# Create your views here.
class IndexView (ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return Question.objects.exclude(choice__isnull= True).filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView (DetailView):
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultView (DetailView):
    model = Question
    template_name = 'polls/result.html'

def vote(request, question_id):
    question = get_object_or_404 (Question, id = question_id)
    try:
        selected_choice = question.choice_set.get (pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
        'question':question,
        'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('result', args=(question_id,)))
