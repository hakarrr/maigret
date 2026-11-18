import logging
from pathlib import Path
from unittest.mock import Mock

import pytest

from maigret.checking import process_site_result
from maigret.result import MaigretCheckStatus, SiteResult
from maigret.sites import MaigretDatabase


@pytest.mark.parametrize('username', ['zavitay', 'noonewouldeverusethis7'])
@pytest.mark.parametrize('status_code', [200, 403])
def test_motorka_login_wall_is_unknown(username, status_code):
    path = Path(__file__).parents[1] / 'maigret/resources/data.json'
    db = MaigretDatabase().load_from_path(str(path))
    site = db.sites_dict['Motorka']
    login_marker = 'Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.'
    info: SiteResult = {
        'username': username,
        'parsing_enabled': False,
        'url_user': site.url.format(
            username=username, urlMain=site.url_main, urlSubpath=site.url_subpath
        ),
    }

    result = process_site_result(
        (login_marker, status_code, None),
        Mock(),
        logging.getLogger(__name__),
        info,
        site,
    )

    assert result['status'].status == MaigretCheckStatus.UNKNOWN
    assert 'Login required' in str(result['status'].error)


def test_motorka_not_enabled_by_default():
    path = Path(__file__).parents[1] / 'maigret/resources/data.json'
    db = MaigretDatabase().load_from_path(str(path))
    assert db.sites_dict['Motorka'].disabled
