from nba_api.custom_configurations.configuration import NBAAPIConfiguration


def test_singleton():
    NBAAPIConfiguration(sleep=5)

    assert NBAAPIConfiguration().sleep == 5

    NBAAPIConfiguration(sleep=10)

    assert NBAAPIConfiguration().sleep == 5
