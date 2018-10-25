from celly.cog import Cog
from celly.file import File
from celly.rating import normalize_rating
from celly.pages import env
from celly.pages.team import team_page, team_rating_graph
from celly.cogs.teams import team_svg


class TeamRenderCog(Cog):
    def __call__(self, teams):
        temp = env.get_template("team.jinja2")

        team_pages = []
        for id, team in teams.items():
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
