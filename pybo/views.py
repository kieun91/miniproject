from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
import openpyxl
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.urls import reverse

def export_to_excel(request):
    questions = Question.objects.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Questions"

    ws.append(["번호", "제목", "작성일시"])

    for question in questions:
        create_date_without_tz = question.create_date.replace(tzinfo=None)
        ws.append([question.id, question.subject, create_date_without_tz])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="questions.xlsx"'
    wb.save(response)
    return response
def index(request):
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('pybo:detail', question_id=question.id)

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

def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    answers = question.answer_set.all()

    for answer in answers:
        answer.delete()


    question.delete()
    return HttpResponseRedirect(reverse('pybo:index'))