import matplotlib.pyplot as plt

from celly.cog import Cog
from celly.file import File
from celly.rating import normalize_rating
from celly.pages import env
from celly.pages.team import team_page, team_rating_graph, team_rating_graph_icon
from celly.cogs.teams import team_svg


# TODO: move this to a Cog
def team_ratings(id, ratings):
    team_ratings_by_date = {}
    dates = []
    team_ratings = []
    plt.xticks(rotation=270)
    for date, rating in ratings.items():
        team_rating = rating[id]
        dates.append(date)
        r = normalize_rating(team_rating["rating"])
        team_ratings.append(r)
    l = plt.plot(dates, team_ratings, 'ro-',  label='line 2')
    # for teams page
    plt.savefig(
        "build/{}".format(team_rating_graph(id)),
        bbox_inches = "tight"
    )
    # for icon
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)
    plt.setp(l, linewidth=12, color='r')
    plt.savefig("build/{}".format(team_rating_graph_icon(id)))
    plt.clf()


class TeamRenderCog(Cog):
    def __call__(self, teams, ratings):
        temp = env.get_template("team.jinja2")

        team_pages = []
        for id, team in teams.items():
            team_ratings(id, ratings)
            abbr = team["abbreviation"]
            r = temp.render(
                team=team,
                img_src=team_svg(id),
                graph_src=team_rating_graph(id),
            )
            page = File(
                name=team_page(abbr),
                src=r,
            )
            team_pages.append(page)
        return team_pages
