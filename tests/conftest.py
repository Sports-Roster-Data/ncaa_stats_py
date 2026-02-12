"""
Shared pytest fixtures for ncaa_stats_py tests.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock


@pytest.fixture
def fixtures_dir():
    """Return path to fixtures directory"""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_teams_html(fixtures_dir):
    """Load sample teams page HTML"""
    teams_file = fixtures_dir / "html_samples" / "teams_page.html"
    if teams_file.exists():
        with open(teams_file) as f:
            return f.read()
    # Return minimal mock HTML if fixture doesn't exist yet
    return """
    <html>
        <body>
            <select id="school_id">
                <option value="">Select School</option>
                <option value="1">Test University</option>
                <option value="2">Sample College</option>
            </select>
        </body>
    </html>
    """


@pytest.fixture
def sample_roster_html(fixtures_dir):
    """Load sample roster page HTML"""
    roster_file = fixtures_dir / "html_samples" / "roster_page.html"
    if roster_file.exists():
        with open(roster_file) as f:
            return f.read()
    # Return minimal mock HTML if fixture doesn't exist yet
    return """
    <html>
        <body>
            <table>
                <tr><th>Name</th><th>Position</th></tr>
                <tr><td>John Doe</td><td>P</td></tr>
                <tr><td>Jane Smith</td><td>1B</td></tr>
            </table>
        </body>
    </html>
    """


@pytest.fixture
def sample_player_stats_html(fixtures_dir):
    """Load sample player stats page HTML"""
    stats_file = fixtures_dir / "html_samples" / "player_stats_page.html"
    if stats_file.exists():
        with open(stats_file) as f:
            return f.read()
    # Return minimal mock HTML if fixture doesn't exist yet
    return """
    <html>
        <body>
            <table>
                <tr><th>Player</th><th>GP</th><th>AVG</th></tr>
                <tr><td>John Doe</td><td>10</td><td>.300</td></tr>
                <tr><td>Jane Smith</td><td>12</td><td>.350</td></tr>
            </table>
        </body>
    </html>
    """


@pytest.fixture
def mock_stat_ids():
    """Return test stat ID mappings"""
    return {
        "baseball": {
            2024: {"batting": 15080, "pitching": 15081, "fielding": 15082},
            2025: {"batting": 15687, "pitching": 15688, "fielding": 15689},
        },
        "mbb": {2024: {"season": 2024}, 2025: {"season": 2025}},
        "wbb": {2024: {"season": 2024}, 2025: {"season": 2025}},
        "mens_lacrosse": {
            2024: {"goalkeepers": 15167, "non_goalkeepers": 15166},
            2025: {"goalkeepers": 15650, "non_goalkeepers": 15649},
            2026: {"goalkeepers": 15808, "non_goalkeepers": 15807},
        },
        "womens_lacrosse": {
            2024: {"goalkeepers": 15155, "non_goalkeepers": 15154, "team": 16541},
            2025: {"goalkeepers": 15648, "non_goalkeepers": 15647, "team": 16780},
        },
    }


@pytest.fixture
def mock_webpage_response():
    """Return mock Playwright response object"""
    response = Mock()
    response.status = 200
    response.text = "<html><body>Mock NCAA Page</body></html>"
    return response


@pytest.fixture
def temp_cache_dir(tmp_path, monkeypatch):
    """
    Create temporary cache directory for tests.

    This fixture:
    - Creates a temporary .ncaa_stats_py directory
    - Sets HOME environment variable to use temp directory
    - Ensures tests don't pollute real cache
    """
    cache_dir = tmp_path / ".ncaa_stats_py"
    cache_dir.mkdir()
    monkeypatch.setenv("HOME", str(tmp_path))
    return cache_dir


@pytest.fixture
def mock_get_webpage(monkeypatch):
    """
    Fixture to mock _get_webpage function across modules.

    Usage:
        def test_something(mock_get_webpage):
            mock_get_webpage.return_value = Mock(text="<html>...</html>", status=200)
            # Your test code here
    """
    mock = Mock()

    # Mock for all sport modules
    modules = [
        "ncaa_stats_py.baseball",
        "ncaa_stats_py.basketball",
        "ncaa_stats_py.football",
        "ncaa_stats_py.soccer",
        "ncaa_stats_py.volleyball",
        "ncaa_stats_py.lacrosse",
        "ncaa_stats_py.field_hockey",
        "ncaa_stats_py.hockey",
        "ncaa_stats_py.softball",
        "ncaa_stats_py.utls",
    ]

    for module in modules:
        monkeypatch.setattr(f"{module}._get_webpage", mock)

    return mock
