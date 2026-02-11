import pytest

from restApi.service import CalculateSummary
from restApi.tests.data import testData
from pprint import pprint


def test_calculate_summary_single_day_single_item():

    per_day, diff = CalculateSummary(testData)

    pprint(diff, width=60, sort_dicts=False, compact=False)
    # print(diff)

    # assert isinstance(per_day, list)
    # assert per_day[0]["cumulative"]["item_mass"] == pytest.approx(100.0)
    # assert per_day[0]["B"]["protein"] == pytest.approx(10.0)

    # assert isinstance(diff, dict)
    # assert diff["cumulative"]["item_massSum"] == pytest.approx(100.0)