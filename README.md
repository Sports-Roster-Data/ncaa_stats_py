# ncaa_stats_py
Allows a user to download and parse data from the National Collegiate Athletics Association (NCAA), and it's member sports.

# Basic Setup

## How to Install

This package is is available through the
[`pip` package manager](https://en.wikipedia.org/wiki/Pip_(package_manager)),
and can be installed through one of the following commands
in your terminal/shell:

```bash
pip install ncaa_stats_py
```

OR

```bash
python -m pip install ncaa_stats_py
```

If you are using a Linux/Mac instance,
you may need to specify `python3` when installing, as shown below:

```bash
python3 -m pip install ncaa_stats_py
```

Alternatively, `ncaa_stats_py` can be installed from
this GitHub repository with the following command through pip:

```bash
pip install git+https://github.com/Sports-Roster-Data/ncaa_stats_py
```

OR

```bash
python -m pip install git+https://github.com/Sports-Roster-Data/ncaa_stats_py
```

OR

```bash
python3 -m pip install git+https://github.com/Sports-Roster-Data/ncaa_stats_py
```

## Supported Sports

`ncaa_stats_py` provides comprehensive data access for 9 NCAA sports:

- **Baseball** (MBA)
- **Basketball** (MBB - Men's Basketball, WBB - Women's Basketball)
- **Field Hockey** (WFH - Women's Field Hockey)
- **Football** (American Football)
- **Hockey** (MIH - Men's Ice Hockey, WIH - Women's Ice Hockey)
- **Lacrosse** (MLA - Men's Lacrosse, WLA - Women's Lacrosse)
- **Soccer** (MSO - Men's Soccer, WSO - Women's Soccer)
- **Softball** (Women's Softball)
- **Volleyball** (MVB - Men's Volleyball, WVB - Women's Volleyball)

## How to Use

`ncaa_stats_py` separates itself by doing the following
things when attempting to get data:
1. Automatically caching any data that is already parsed
2. Automatically forcing a 5 second sleep timer for any HTML call,
    to ensure that any function call from this package
    won't result in you getting IP banned
    (you do not *need* to add sleep timers if you're looping through,
    and calling functions in this python package).
3. Automatically refreshing any cached data if the data hasn't been refreshed in a while.

### Baseball Example

For example, the following code will work as-is,
    and in the second loop, the code will load in the teams
    even faster because the data is cached
    on the device you're running this code.

```python
from timeit import default_timer as timer

from ncaa_stats_py.baseball import (
    get_baseball_team_roster,
    get_baseball_teams
)

start_time = timer()

# Loads in a table with every DI NCAA baseball team in the 2024 season.
# If this is the first time you run this script,
# it may take some time to repopulate the NCAA baseball team information data.

teams_df = get_baseball_teams(season=2024, level="I")

end_time = timer()

time_elapsed = end_time - start_time
print(f"Elapsed time: {time_elapsed:03f} seconds.\n\n")

# Gets 5 random D1 teams from 2024
teams_df = teams_df.sample(5)
print(teams_df)
print()


# Let's send this to a list to make the loop slightly faster
team_ids_list = teams_df["team_id"].to_list()

# First loop
# If the data isn't cached, it should take 35-40 seconds to do this loop
start_time = timer()

for t_id in team_ids_list:
    print(f"On Team ID: {t_id}")
    df = get_baseball_team_roster(team_id=t_id)
    # print(df)

end_time = timer()

time_elapsed = end_time - start_time
print(f"Elapsed time: {time_elapsed:03f} seconds.\n\n")

# Second loop
# Because the data has been parsed and cached,
# this shouldn't take that long to loop through
start_time = timer()

for t_id in team_ids_list:
    print(f"On Team ID: {t_id}")
    df = get_baseball_team_roster(team_id=t_id)
    # print(df)

end_time = timer()
time_elapsed = end_time - start_time
print(f"Elapsed time: {time_elapsed:03f} seconds.\n\n")

```

### Basketball Example

Basketball supports both men's and women's divisions:

```python
from ncaa_stats_py.basketball import get_basketball_teams, get_basketball_player_season_stats

# Get women's basketball teams for 2024
womens_teams_df = get_basketball_teams(season=2024, level="I", get_womens_basketball_data=True)
print(womens_teams_df.head())

# Get men's basketball teams for 2024
mens_teams_df = get_basketball_teams(season=2024, level="I", get_womens_basketball_data=False)
print(mens_teams_df.head())
```

### Soccer Example

Soccer also supports both men's and women's divisions with additional match-level statistics:

```python
from ncaa_stats_py.soccer import get_soccer_teams, get_soccer_match_stats

# Get women's soccer teams
womens_soccer_df = get_soccer_teams(season=2024, level="I", get_womens_soccer_data=True)
print(womens_soccer_df.head())

# Get match statistics for a specific game
match_stats_df = get_soccer_match_stats(game_id=12345)
print(match_stats_df)
```

### Volleyball Example

Volleyball includes a configuration system for setting default preferences:

```python
from ncaa_stats_py.volleyball import configure_volleyball, get_volleyball_teams

# Configure volleyball to default to women's volleyball
configure_volleyball(default_sport="women")

# Get volleyball teams for 2024
teams_df = get_volleyball_teams(season=2024, level="I")
print(teams_df.head())
```

### Football Example

```python
from ncaa_stats_py.football import get_football_teams, get_football_team_schedule

# Get Division I football teams for 2024
teams_df = get_football_teams(season=2024, level="I")
print(teams_df.head())

# Get schedule for a specific team
schedule_df = get_football_team_schedule(team_id=123)
print(schedule_df)
```

# Dependencies

`ncaa_stats_py` is dependent on the following python packages:
- [`beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/): To assist with parsing HTML data.
- [`lxml`](https://lxml.de/): To work with `beautifulsoup4` in assisting with parsing HTML data.
- [`pandas`](https://github.com/pandas-dev/pandas): For `DataFrame` creation within package functions.
- [`pytz`](https://pythonhosted.org/pytz/): Used to attach timezone information for any date/date time objects encountered by this package.
- [`requests`](https://github.com/psf/requests): Used to make HTTPS requests.
- [`tqdm`](https://github.com/tqdm/tqdm): Used to show progress bars for actions in functions that are known to take minutes to load.

# License

This package is licensed under the MIT license. You can view the package's license [here](https://github.com/SportsRosterData/ncaa_stats_py/blob/main/LICENSE).

# Documentation

For more information about this package, its functions, and ways you can use said functions can be found at [https://SportsRosterData.github.io/ncaa_stats_py/](https://SportsRosterData.github.io/ncaa_stats_py/).