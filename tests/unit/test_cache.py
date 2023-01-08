import time

from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonType


def test_cache():
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

