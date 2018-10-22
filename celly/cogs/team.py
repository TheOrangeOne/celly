import matplotlib.pyplot as plt

from celly.cog import Cog
from celly.file import File
from celly.rating import normalize_rating
from celly.pages import env
from celly.pages.team import team_page
from celly.cogs.teams import team_svg


def team_rating_graph_file(id):
    return "{}_rating.png".format(id)


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
    plt.plot(dates, team_ratings, 'ro-',  label='line 2')
    plt.savefig("build/{}".format(team_rating_graph_file(id)))
    plt.clf()


class TeamRenderCog(Cog):
    def output(self, teams, ratings):
        temp = env.get_template("team.jinja2")

        team_pages = []
        for id, team in teams.items():
            team_ratings(id, ratings)
            abbr = team["abbreviation"]
            r = temp.render(
                team=team,
                img_src=team_svg(id),
                graph_src="{}".format(team_rating_graph_file(id)),
            )
            page = File(
                name=team_page(abbr),
                src=r,
            )
            team_pages.append(page)
        return team_pages
