from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from company.permissions import IsCeoOrIsManagerOrIsEmployee
from schedules.models import Schedule
from timesheets.models import Timesheet
from timesheets.serializers import TimesheetSerializer

"""
Rules:
1. Check timesheet date against schedule workdays
2. Check timesheet times against schedule hours
3. Check timesheet total_hours against schedule total_hours to get overtime
4. Employee checks in once per shift and checks out once per shift
5. Automatically record the checkin and checkout time
6. Automatically calculate the total_hours
7. Prevent checkin changes
8. Use server time
"""


class CheckinView(APIView):
    permission_classes = [
        IsCeoOrIsManagerOrIsEmployee,
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        serializer = TimesheetSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            shift = serializer.validated_data.get("shift")
            date = serializer.validated_data.get("date")

            # checking if the shift and date are valid
            try:
                shift = Schedule.objects.get(reference=shift)
            except Schedule.DoesNotExist:
                return Response(
                    {"detail": "Invalid shift."}, status=status.HTTP_400_BAD_REQUEST
                )

            # Extract the day of the week from the date
            day = date.strftime("%A")

            # Check if the day of the week is a workday
            workdays = shift.workdays  # get the workdays from the shift(JSON)
            if day not in workdays:
                return Response(
                    {"detail": "Invalid workday."}, status=status.HTTP_400_BAD_REQUEST
                )

            # Check if user has already checked in
            timesheet, created = Timesheet.objects.get_or_create(
                user=user, shift=shift, date=date, defaults={"checkin": timezone.now()}
            )

            if not created:
                if timesheet.checkin and timesheet.checkout:
                    return Response(
                        {"detail": "User has already checked out."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                elif timesheet.checkin:
                    return Response(
                        {"detail": "User has already checked in."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    timesheet.checkin = timezone.now()
                    timesheet.save()
                    return Response(
                        {"detail": "User has checked in successfully."},
                        status=status.HTTP_200_OK,
                    )
            else:
                return Response(
                    {"detail": "User has checked in successfully."},
                    status=status.HTTP_200_OK,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CheckoutView(APIView):
#     permission_classes = [IsAuthenticated, IsCeoOrIsManagerOrIsEmployee]

#     def patch(self, request, *args, **kwargs):
#         serializer = TimesheetSerializer(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             shift = serializer.validated_data.get("shift")
#             date = serializer.validated_data.get("date")

#             try:
#                 shift = Schedule.objects.get(reference=shift)
#             except Schedule.DoesNotExist:
#                 return Response(
#                     {"detail": "Invalid shift."}, status=status.HTTP_400_BAD_REQUEST
#                 )
