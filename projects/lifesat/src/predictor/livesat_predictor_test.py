import pytest


class TestLivesatPredictor:
    @pytest.mark.unit
    def test_dummy(self):
        assert True

    @pytest.mark.skip
    def test_dummy_skip(self):
        assert 1 == 2
