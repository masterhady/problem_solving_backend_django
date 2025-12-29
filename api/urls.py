
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .auth_views import RegisterView, LoginView
from .views.coding_profile_views import CodingProfileViewSet
from .views.company_coding_analysis_views import CompanyLeetCodeAnalysisView, CompanyLeetCodeExportView
from .views.employee_progress_views import (
    EmployeeViewSet, EmployeeProgressView, KPIDashboardView, SyncEmployeeView
)
from .views.employee_goal_views import EmployeeGoalViewSet
from .views.diagnostic_views import DbStatusView

router = DefaultRouter()
router.register(r'coding-profiles', CodingProfileViewSet, basename='coding-profiles')

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="auth_register"),
    path("auth/login/", LoginView.as_view(), name="auth_login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # Company LeetCode Analysis
    path("company/leetcode/analyze/", CompanyLeetCodeAnalysisView.as_view(), name="company_leetcode_analyze"),
    path("company/leetcode/export/", CompanyLeetCodeExportView.as_view(), name="company_leetcode_export"),
    
    # Employee Management & Progress Tracking
    path("company/employees/", EmployeeViewSet.as_view(), name="company_employees"),
    path("company/employees/<uuid:employee_id>/", EmployeeViewSet.as_view(), name="company_employee_detail"),
    path("company/employees/<uuid:employee_id>/sync/", SyncEmployeeView.as_view(), name="company_employee_sync"),
    path("company/employees/<uuid:employee_id>/progress/", EmployeeProgressView.as_view(), name="company_employee_progress"),
    path("company/progress/", EmployeeProgressView.as_view(), name="company_progress_all"),
    path("company/kpi-dashboard/", KPIDashboardView.as_view(), name="company_kpi_dashboard"),
    
    # Employee Goals
    path("company/employees/<uuid:employee_id>/goals/", EmployeeGoalViewSet.as_view(), name="company_employee_goals"),
    path("company/goals/", EmployeeGoalViewSet.as_view(), name="company_goals_all"),
    path("company/goals/<uuid:goal_id>/", EmployeeGoalViewSet.as_view(), name="company_goal_detail"),
    
    path("db-status/", DbStatusView.as_view(), name="db_status"),
    
    path("", include(router.urls)),
]
