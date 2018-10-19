def format_rating(rating):
    rating_f = "{:4.2f}".format(rating)
    return rating_f

def format_diff(diff):
    if diff == 0.0:
        return ''
    plus = "+" if diff > 0 else "-"
    diff_f = "{}{:4.2f}".format(plus, abs(diff))
    return diff_f

def ratings_page(date):
    return "{}-ratings.html".format(date)
