fantasy-football
================

I use to take part in a fantasy football salary cap league. In this format, you
have a fixed budget with which to purchase/hire players subject to constraints
on the number of players for each position. Unlike other leagues, multiple
teams in the same league can have the same player. I was curious to see how
well a binary integer linear programming approach to team selection would fair
against 'expert' pickers.

The code uses python to scrape the player's current weekly price from the Yahoo
Fantasy Football Salary Cap interface. Because you have to be logged in to
access these pages, the code reads in a cookie file that is exported from your
browser. There is a seperate utility to scrape projects from CBS's fantasy
football page. Using this data, an LP model is constructed and solved using
`lp_solve`. Finally, this solution is verified as being feasible and then saved
to file. You can then make the appropriate selections through the league's web
interface.

These steps are wrapped up for you in the script `coach-ditka.sh`.

Overall, this strategy did OK, but they probably had more to do with a general
lack of interest from most of the other league members in making their team
selections. A major issue with this approach is that it 'myopic', choosing to
optimize this weeks performance without regard to future weeks.
