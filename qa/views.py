# qa/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Question, Answer, Like
from .forms import CustomUserCreationForm, QuestionForm, AnswerForm
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'qa/home.html', {'questions': questions})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'qa/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'qa/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'qa/ask_question.html', {'form': form})

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'qa/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_form'] = AnswerForm()
        return context

@login_required
def post_answer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', pk=question.pk)
    return redirect('question_detail', pk=question.pk)

@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    like, created = Like.objects.get_or_create(user=request.user, answer=answer)
    
    if not created:
        like.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'likes_count': answer.likes.count(),
            'is_liked': created
        })
    
    return redirect('question_detail', pk=answer.question.pk)