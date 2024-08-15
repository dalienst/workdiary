from datetime import datetime

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
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
9. Prevent checkin after shift end time in a day: only checkin on or after the shift start time but not after the shift end time. One has to wait for the next shift.
10. Confirm if user belongs to the shift company
"""


class TimesheetList(generics.ListAPIView):
    serializer_class = TimesheetSerializer
    queryset = Timesheet.objects.all()
    permission_classes = [
        IsCeoOrIsManagerOrIsEmployee,
        IsAuthenticated,
    ]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


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
            checkin_time = timezone.now().time()

            # checking if the shift and date are valid
            try:
                shift = Schedule.objects.get(reference=shift.reference)
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

            # Check if the user belongs to the shift company
            if not (
                user.companies.filter(id=shift.company.id).exists()
                or user.company.filter(id=shift.company.id).exists()
            ):
                return Response(
                    {"detail": "User does not belong to the shift company."},
                    status=status.HTTP_400_BAD_REQUEST,
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
                # TODO: Ask for help from Lewis
                # prevent checkin after shift end time in a day before or on the shift start time
                elif checkin_time > datetime.combine(date, shift.end_time).time():
                    return Response(
                        {"detail": "You cannot check in after the shift end time."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                elif timesheet.checkin:
                    # check if user has already checked in
                    return Response(
                        {
                            "detail": "User has already checked in.",
                            "slug": timesheet.slug,
                            "reference": timesheet.reference,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:

                    checkin_time = timezone.now()
                    if checkin_time > shift.start_time:
                        timesheet.status = "Late"
                    else:
                        timesheet.status = "Regular"

                    timesheet.checkin = timezone.now()
                    timesheet.save()
                    serialized_timesheet = TimesheetSerializer(timesheet).validated_data
                    return Response(
                        serialized_timesheet,
                        status=status.HTTP_200_OK,
                    )
            else:
                checkin_time = timezone.now().time()
                if checkin_time > shift.start_time:
                    timesheet.status = "Late"
                else:
                    timesheet.status = "Regular"

                timesheet.checkin = timezone.now()
                timesheet.save()
                # TODO: Ask Lewis on serializing
                return Response(
                    {
                        "detail": "User has checked in successfully.",
                        "slug": timesheet.slug,
                        "reference": timesheet.reference,
                    },
                    status=status.HTTP_200_OK,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckoutView(generics.RetrieveUpdateAPIView):
    queryset = Timesheet.objects.all()
    serializer_class = TimesheetSerializer
    permission_classes = [
        IsAuthenticated,
        IsCeoOrIsManagerOrIsEmployee,
    ]
    lookup_field = "slug"

    def get_queryset(self):
        return Timesheet.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if already checked out
        if instance.checkout:
            return Response(
                {"detail": "User has already checked out."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Automatically check out
        instance.checkout = timezone.now()

        # Calculate total hours
        total_hours = (instance.checkout - instance.checkin).total_seconds() / 3600
        instance.total_hours = round(total_hours, 2)

        # Determine if this time qualifies as overtime based on the shift's schedule
        start_time = datetime.combine(instance.date, instance.shift.start_time)
        end_time = datetime.combine(instance.date, instance.shift.end_time)
        shift_duration = (end_time - start_time).total_seconds() / 3600

        if total_hours > shift_duration:
            instance.is_overtime = True

        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FinanceTimeSheetListView(generics.ListAPIView):
    queryset = Timesheet.objects.all()
    serializer_class = TimesheetSerializer
    permission_classes = [
        IsAuthenticated,
        IsCeoOrIsManagerOrIsEmployee,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "date",
        "user__first_name",
        "user__last_name",
        "shift__reference",
        "is_overtime",
        "status",
    ]
