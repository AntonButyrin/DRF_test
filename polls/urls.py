from django.urls import path

from polls import views

app_name = 'polls'
urlpatterns = [
    path('', views.login, name='login'),

    path('polls/create/', views.poll_create, name='poll_create'),
    path('choice/create/', views.choice_create, name='choice_create'),
    path('question/create/', views.question_create, name='question_create'),
    path('answer/create/', views.answer_create, name='answer_create'),

    path('polls/update/<int:poll_id>/', views.poll_update, name='poll_update'),
    path('question/update/<int:question_id>/', views.question_update, name='question_update'),
    path('choice/update/<int:choice_id>/', views.choice_update, name='choice_update'),
    path('answer/update/<int:answer_id>/', views.answer_update, name='answer_update'),

    path('polls/view/', views.poll_view, name='poll_view'),
    path('polls/view/active/', views.active_poll_view, name='active_poll_view'),
    path('answer/view/<int:user_id>/', views.answer_view, name='answer_view')
]
