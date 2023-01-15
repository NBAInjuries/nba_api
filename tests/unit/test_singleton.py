from nba_api.nba_api import NBAApi


def test_singleton():
    NBAApi(sleep=5)

    assert NBAApi().sleep == 5

    NBAApi(sleep=10)

    assert NBAApi().sleep == 5
