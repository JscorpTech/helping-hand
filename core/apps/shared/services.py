from django.db.models.functions import ExtractHour, ExtractMonth, ExtractDay
from core.apps.sos.models import UserRequestModel
from datetime import datetime, timedelta
from django.db.models import Count


def get_userrequest_chart_data(period):
    if period == "day":
        labels = [f"{i}:00" for i in range(24)]
        data = (
            UserRequestModel.objects.filter(created_at__date=datetime.today())
            .annotate(hour=ExtractHour("created_at"))
            .values("hour")
            .annotate(count=Count("id"))
        )
        counts = {item["hour"]: item["count"] for item in data}
        chart_data = [counts.get(hour, 0) for hour in range(24)]

    elif period == "week":
        labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        start_date = datetime.today() - timedelta(days=datetime.today().weekday())
        end_date = start_date + timedelta(days=6)
        data = (
            UserRequestModel.objects.filter(created_at__date__range=[start_date, end_date])
            .annotate(weekday=ExtractDay("created_at"))
            .values("weekday")
            .annotate(count=Count("id"))
        )
        counts = {item["weekday"]: item["count"] for item in data}
        chart_data = [counts.get(day, 0) for day in range(1, 8)]

    elif period == "month":
        labels = [f"Day {i}" for i in range(1, 32)]
        data = (
            UserRequestModel.objects.filter(
                created_at__year=datetime.today().year, created_at__month=datetime.today().month
            )
            .annotate(day=ExtractDay("created_at"))
            .values("day")
            .annotate(count=Count("id"))
        )
        counts = {item["day"]: item["count"] for item in data}
        chart_data = [counts.get(day, 0) for day in range(1, 32)]

    elif period == "year":
        labels = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        data = (
            UserRequestModel.objects.filter(created_at__year=datetime.today().year)
            .annotate(month=ExtractMonth("created_at"))
            .values("month")
            .annotate(count=Count("id"))
        )
        counts = {item["month"]: item["count"] for item in data}
        chart_data = [counts.get(month, 0) for month in range(1, 13)]

    else:
        labels = []
        chart_data = []

    return labels, chart_data
