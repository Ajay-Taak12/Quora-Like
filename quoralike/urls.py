# quoralike/urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from qa import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='qa/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('ask/', views.ask_question, name='ask_question'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('question/<int:pk>/answer/', views.post_answer, name='post_answer'),
    path('like/<int:answer_id>/', views.like_answer, name='like_answer'),
]