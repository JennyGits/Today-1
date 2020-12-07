from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from bs4 import BeautifulSoup
from polls.models import Question, Choice
from django.utils import timezone

def main(request):
    return render(request, 'polls/main.html')

def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def result(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]

    for q in latest_question_list:
        total = 0
        choice = Choice.objects.all().filter(question = q)

        for c in choice:
            total += c.votes

        for c in choice:
            c.proportion = round(c.votes / total * 100)
            c.save()

    context = {'questions': latest_question_list}
    return render(request, 'polls/result.html', context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    cho_id = request.POST.get('choice')
    choice = get_object_or_404(Choice, pk=cho_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:index'))

def addQuestion(request):
    return render(request, 'polls/addQuestion.html')

def add(request):
    question = request.POST.get('question')
    choice1 = request.POST.get('choice1')
    choice2 = request.POST.get('choice2')

    q = Question(question_text=question, pub_date=timezone.now())
    q.save()

    c = Choice(question=q, choice_text=choice1)
    c.save()
    c = Choice(question=q, choice_text=choice2)
    c.save()

    return HttpResponseRedirect(reverse('polls:index'))