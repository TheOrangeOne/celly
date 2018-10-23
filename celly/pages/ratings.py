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

def rating_rgb(rating):
    cg = round((rating/100)*255)
    cr = 255-cg
    return "color: rgb({}, {}, 0);".format(cr, cg)

def diff_rgb(diff):
    diff = ((diff+6)/12)*100
    cg = round((diff/100)*255)
    cr = 255-cg
    return "color: rgb({}, {}, 0);".format(cr, cg)
