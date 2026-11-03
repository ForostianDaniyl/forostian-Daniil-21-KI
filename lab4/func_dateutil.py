from datetime import date
from dateutil.relativedelta import relativedelta


def date_demo():
    today = date.today()
    return {
        "today": str(today),
        "+3 місяці": str(today + relativedelta(months=3)),
        "-1 рік": str(today - relativedelta(years=1)),
    }