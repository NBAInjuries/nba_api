import time

from nba_api.library.cache import _generate_cache_key
from nba_api.nba_api import NBAApi
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonType


def test_generate_cache_key():
    params = [('DateFrom', ''), ('DateTo', ''), ('LeagueID', ''), ('PlayerID', 2544), ('Season', 2019), ('SeasonType', 'Regular Season')]
    endpoint = "playergamelog"
    key = _generate_cache_key(params, endpoint)

    assert key == "playergamelog:[('PlayerID', 2544), ('Season', 2019), ('SeasonType', 'Regular Season')]"


def test_local_cache():

    start = time.time()
    game_log_no_cache = playergamelog.PlayerGameLog(
        player_id=2544,
        season=2019,
        season_type_all_star=SeasonType.regular,
    )
    end_no_cache = time.time() - start

    start = time.time()
    game_log_cache = playergamelog.PlayerGameLog(
        player_id=2544,
        season=2019,
        season_type_all_star=SeasonType.regular,
    )
    end_cache = time.time() - start

    assert end_no_cache > end_cache
    assert game_log_no_cache.get_dict() == game_log_cache.get_dict()


def test_persistent_cache():
    # if testing make sure to add cache path

    start = time.time()
    game_log_no_cache = playergamelog.PlayerGameLog(
        player_id=2544,
        season=2019,
        season_type_all_star=SeasonType.regular,
    )
    end_no_cache = time.time() - start

    start = time.time()
    game_log_cache = playergamelog.PlayerGameLog(
        player_id=2544,
        season=2019,
        season_type_all_star=SeasonType.regular,
    )
    end_cache = time.time() - start

    assert end_no_cache > end_cache
    assert game_log_no_cache.get_dict() == game_log_cache.get_dict()
