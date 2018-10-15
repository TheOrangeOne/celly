from datetime import datetime, timedelta


FMT = "%Y-%m-%d"

def ymd_add_n_days(ymd, n):
    date = datetime.strptime(ymd, FMT)
    prev = date + timedelta(days=n)
    return prev.strftime(FMT)


def prev_ymd(ymd):
    return ymd_add_n_days(ymd, -1)


def next_ymd(ymd):
    return ymd_add_n_days(ymd, 1)
