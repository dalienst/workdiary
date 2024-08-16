from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsCeo(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_ceo


class IsCeoOrIsManager(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_ceo or request.user.is_manager


class IsCeoOrIsManagerOrIsEmployee(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return (
            request.user.is_ceo
            or request.user.is_manager
            or request.user.is_employee
            or request.user.is_finance
        )


class IsFinanceOrIsCeo(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_finance or request.user.is_ceo
