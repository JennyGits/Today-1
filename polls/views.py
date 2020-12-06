from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from bs4 import BeautifulSoup
from polls.models import Question, Choice

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

    total = [0 for _ in range(5)]
    i = 0
    j = 0

    for q in latest_question_list:
        choice = Choice.objects.all().filter(question = q)
        for c in choice:
            total[i] += c.votes
        i += 1

        for c in choice:
            c.proportion = round(c.votes / total[j] * 100)
            c.save()
        j += 1

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

