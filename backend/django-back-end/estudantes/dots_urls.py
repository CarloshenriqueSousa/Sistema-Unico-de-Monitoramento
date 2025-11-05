from django.urls import path
from . import dots_views as views

app_name = 'dots'

urlpatterns = [
    path('profile/<int:user_id>/', views.DotsProfileView.as_view(), name='profile'),
    path('leaderboard/', views.DotsLeaderboardView.as_view(), name='leaderboard'),
    path('achievements/', views.DotsAchievementsView.as_view(), name='achievements'),
    path('skills/<int:student_id>/', views.DotsSkillView.as_view(), name='skills'),
    path('skills/<int:student_id>/bulk/', views.DotsSkillBulkView.as_view(), name='skills-bulk'),
    path('sync/<str:service>/', views.DotsSyncView.as_view(), name='sync'),
]


