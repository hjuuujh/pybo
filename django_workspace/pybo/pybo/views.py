from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.utils import timezone
from django.views.generic import ListView, DetailView

from pybo.forms import QuestionForm
from pybo.models import Question


# def index(request):
#     question_list = Question.objects.order_by('-create_date')
#     context = {'question_list': question_list}
#     return render(request, 'pybo/question_list.html', context)
#
# def detail(request, question_id):
#     # question = Question.objects.get(id=question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     context = {'object':question}
#     return render(request, 'pybo/question_detail.html', context)

class IndexView(ListView):
    paginate_by = 10
    def get_queryset(self):
        return Question.objects.order_by('-create_date')


class DetailView(DetailView):
    model = Question


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now(),author=request.user)
    return redirect('pybo:detail', pk=question.id)


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)