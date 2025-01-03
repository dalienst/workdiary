"""
URL configuration for workdiary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/clients/", include("clients.urls")),
    path("api/invoices/", include("invoices.urls")),
    path("api/projects/", include("projects.urls")),
    path("api/tasks/", include("tasks.urls")),
    path("api/company/", include("company.urls")),
    path("api/invitation/", include("invitation.urls")),
    path("api/schedules/", include("schedules.urls")),
    path("api/roles/", include("roles.urls")),
    path("api/timesheets/", include("timesheets.urls")),
    path("api/payroll/", include("payroll.urls")),
]
