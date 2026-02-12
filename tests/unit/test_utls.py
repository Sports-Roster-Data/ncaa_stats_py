"""
Unit tests for ncaa_stats_py.utls module.

Streamlined test suite focusing on critical functionality and error handling.
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch
from ncaa_stats_py.utls import (
    _stat_id_dict,
    _get_stat_id,
    _name_smother,
    _format_folder_str,
    _get_seconds_from_time_str,
    _get_minute_formatted_time_from_seconds,
)


class TestStatIdDict:
    """Test the _stat_id_dict function - core data structure validation"""

    @pytest.mark.unit
    def test_stat_id_dict_returns_dict(self):
        """Test that _stat_id_dict returns a dictionary"""
        result = _stat_id_dict()
        assert isinstance(result, dict)
        assert len(result) > 0

    @pytest.mark.unit
    def test_stat_id_dict_has_all_sports(self):
        """Test that stat_id_dict contains all supported sports"""
        result = _stat_id_dict()
        expected_sports = [
            "baseball",
            "mbb",
            "wbb",
            "field_hockey",
            "mens_hockey",
            "womens_hockey",
            "mens_lacrosse",
            "womens_lacrosse",
            "softball",
        ]
        for sport in expected_sports:
            assert sport in result, f"Sport '{sport}' not found in stat_id_dict"

    @pytest.mark.unit
    def test_stat_id_dict_has_current_season(self):
        """Test that stat_id_dict has entries for recent seasons"""
        result = _stat_id_dict()

        # Check 2024 and 2025 are present for key sports
        assert 2024 in result["baseball"]
        assert 2025 in result["baseball"]
        assert 2024 in result["mbb"]
        assert 2025 in result["mbb"]

    @pytest.mark.unit
    def test_stat_id_dict_structure_baseball(self):
        """Test the structure of baseball stat IDs"""
        result = _stat_id_dict()
        baseball_2024 = result["baseball"][2024]

        assert "batting" in baseball_2024
        assert "pitching" in baseball_2024
        assert "fielding" in baseball_2024
        assert isinstance(baseball_2024["batting"], int)
        assert isinstance(baseball_2024["pitching"], int)
        assert isinstance(baseball_2024["fielding"], int)


class TestGetStatId:
    """Test the _get_stat_id function - critical for all data retrieval"""

    @pytest.mark.unit
    def test_get_stat_id_valid_baseball(self):
        """Test getting valid stat ID for baseball"""
        result = _get_stat_id("baseball", 2024, "batting")
        assert result == 15080

    @pytest.mark.unit
    def test_get_stat_id_invalid_sport(self):
        """Test that invalid sport raises LookupError"""
        with pytest.raises(LookupError, match="Could not locate a stat ID"):
            _get_stat_id("invalid_sport", 2024, "batting")

    @pytest.mark.unit
    def test_get_stat_id_invalid_season(self):
        """Test that invalid season raises LookupError"""
        with pytest.raises(LookupError, match="Could not locate a stat ID"):
            _get_stat_id("baseball", 1900, "batting")

    @pytest.mark.unit
    def test_get_stat_id_invalid_stat_type(self):
        """Test that invalid stat type raises LookupError"""
        with pytest.raises(LookupError, match="Could not locate a stat ID"):
            _get_stat_id("baseball", 2024, "invalid_stat")


class TestNameSmother:
    """Test the _name_smother function - essential for player name parsing"""

    @pytest.mark.unit
    def test_name_smother_simple_name(self):
        """Test simple name without special characters"""
        result = _name_smother("John Doe")
        assert result == "John Doe"

    @pytest.mark.unit
    def test_name_smother_with_suffix(self):
        """Test name with suffix (Jr., Sr., III) - common in NCAA data"""
        result = _name_smother("John Doe, Jr.")
        assert result == "Jr. John Doe"

    @pytest.mark.unit
    def test_name_smother_comma_separated(self):
        """Test comma-separated format (Last, First) - common NCAA format"""
        result = _name_smother("Doe, John")
        assert result == "John Doe"

    @pytest.mark.unit
    def test_name_smother_none_input(self):
        """Test handling of None input - prevents crashes on missing data"""
        result = _name_smother(None)
        assert pd.isna(result)


class TestFormatFolderStr:
    """Test the _format_folder_str function"""

    @pytest.mark.unit
    def test_format_folder_str_trailing_slash(self):
        """Test that trailing slash is preserved - most important case"""
        result = _format_folder_str("/path/to/folder/")
        assert result.endswith("/")


class TestGetSecondsFromTimeStr:
    """Test the _get_seconds_from_time_str function"""

    @pytest.mark.unit
    def test_get_seconds_zero_minutes(self):
        """Test 0:00 time string - edge case"""
        result = _get_seconds_from_time_str("0:00")
        assert result == 0

    @pytest.mark.unit
    def test_get_seconds_multiple_minutes(self):
        """Test multiple minutes with seconds - basic functionality"""
        result = _get_seconds_from_time_str("5:30")
        assert result == 330


class TestGetMinuteFormattedTimeFromSeconds:
    """Test the _get_minute_formatted_time_from_seconds function"""

    @pytest.mark.unit
    def test_format_time_zero_seconds(self):
        """Test 0 seconds formats to 00:00 - edge case"""
        result = _get_minute_formatted_time_from_seconds(0)
        assert result == "00:00"

    @pytest.mark.unit
    def test_format_time_multiple_minutes(self):
        """Test multiple minutes - basic functionality"""
        result = _get_minute_formatted_time_from_seconds(330)
        assert result == "05:30"


class TestGetSchools:
    """Test the _get_schools function - critical caching functionality"""

    @pytest.mark.unit
    @patch('ncaa_stats_py.utls._get_webpage')
    @patch('ncaa_stats_py.utls.exists')
    @patch('ncaa_stats_py.utls.getmtime')
    @patch('ncaa_stats_py.utls.expanduser')
    def test_get_schools_cache_hit_fresh(self, mock_expanduser, mock_getmtime, mock_exists, mock_webpage, tmp_path, monkeypatch):
        """Test that fresh cache is loaded without making web request"""
        from ncaa_stats_py.utls import _get_schools
        import time

        # Setup mock home directory
        mock_expanduser.return_value = str(tmp_path)
        cache_dir = tmp_path / ".ncaa_stats_py"
        cache_dir.mkdir()
        cache_file = cache_dir / "schools.csv"

        # Create a mock cached CSV
        cached_data = pd.DataFrame({
            'school_id': [100, 101, 102],
            'school_name': ['Test University', 'Sample College', 'Example State']
        })
        cached_data.to_csv(cache_file, index=False)

        # Mock that cache file exists and is recent (< 90 days old)
        mock_exists.side_effect = lambda path: True
        mock_getmtime.return_value = time.time() - (60 * 86400)  # 60 days old

        # Call function
        result = _get_schools()

        # Assert: should load from cache, not make web request
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert 'school_id' in result.columns
        assert 'school_name' in result.columns
        mock_webpage.assert_not_called()

    @pytest.mark.unit
    @patch('ncaa_stats_py.utls._get_webpage')
    @patch('ncaa_stats_py.utls.expanduser')
    def test_get_schools_cache_miss(self, mock_expanduser, mock_webpage, tmp_path, monkeypatch):
        """Test fetching schools when no cache exists"""
        from ncaa_stats_py.utls import _get_schools

        # Setup mock home directory
        mock_expanduser.return_value = str(tmp_path)

        # Mock web response
        mock_html = """
        <html>
            <select name="org_id" id="org_id_select">
                <option value="">Select School</option>
                <option value="100">Test University</option>
                <option value="101">Sample College</option>
            </select>
        </html>
        """
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.status = 200
        mock_webpage.return_value = mock_response

        # Call function
        result = _get_schools()

        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) >= 1
        mock_webpage.assert_called_once()

    @pytest.mark.unit
    @patch('ncaa_stats_py.utls._get_webpage')
    @patch('ncaa_stats_py.utls.exists')
    @patch('ncaa_stats_py.utls.getmtime')
    @patch('ncaa_stats_py.utls.expanduser')
    def test_get_schools_cache_expired(self, mock_expanduser, mock_getmtime, mock_exists, mock_webpage, tmp_path, monkeypatch):
        """Test that expired cache triggers web request"""
        from ncaa_stats_py.utls import _get_schools
        import time

        # Setup mock home directory
        mock_expanduser.return_value = str(tmp_path)
        cache_dir = tmp_path / ".ncaa_stats_py"
        cache_dir.mkdir()
        cache_file = cache_dir / "schools.csv"

        # Create an old cached CSV
        cached_data = pd.DataFrame({
            'school_id': [100],
            'school_name': ['Old School']
        })
        cached_data.to_csv(cache_file, index=False)

        # Mock that cache file exists but is old (> 90 days)
        mock_exists.side_effect = lambda path: True
        mock_getmtime.return_value = time.time() - (100 * 86400)  # 100 days old

        # Mock web response
        mock_html = """
        <html>
            <select name="org_id" id="org_id_select">
                <option value="100">Test University</option>
                <option value="101">Sample College</option>
            </select>
        </html>
        """
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.status = 200
        mock_webpage.return_value = mock_response

        # Call function
        result = _get_schools()

        # Assert: should make web request due to expired cache
        assert isinstance(result, pd.DataFrame)
        mock_webpage.assert_called_once()
        assert 'school_id' in result.columns
        assert 'school_name' in result.columns

    @pytest.mark.unit
    @patch('ncaa_stats_py.utls._get_webpage')
    @patch('ncaa_stats_py.utls.expanduser')
    def test_get_schools_handles_http_error(self, mock_expanduser, mock_webpage, tmp_path):
        """Test error handling when HTTP request fails"""
        from ncaa_stats_py.utls import _get_schools

        # Setup mock home directory
        mock_expanduser.return_value = str(tmp_path)

        # Mock web response with error
        mock_webpage.side_effect = ConnectionError("HTTP 500 Internal Server Error")

        # Call function and expect error
        with pytest.raises(ConnectionError):
            _get_schools()


class TestGetWebpage:
    """Test the _get_webpage function error handling"""

    @pytest.mark.unit
    @patch('ncaa_stats_py.utls._get_browser')
    def test_get_webpage_http_400_error(self, mock_get_browser):
        """Test handling of HTTP 400 Bad Request error"""
        from ncaa_stats_py.utls import _get_webpage

        # Mock browser and context
        mock_page = Mock()
        mock_response = Mock()
        mock_response.status = 400
        mock_page.goto.return_value = mock_response
        mock_page.content.return_value = "<html><body>Bad Request</body></html>"

        mock_context = Mock()
        mock_context.new_page.return_value = mock_page

        mock_browser = Mock()
        mock_get_browser.return_value = (mock_browser, mock_context)

        # Call function and expect ConnectionRefusedError
        with pytest.raises(ConnectionRefusedError, match="HTTP 400"):
            _get_webpage("https://example.com/bad-request")

    @pytest.mark.unit
    @patch('ncaa_stats_py.utls._get_browser')
    def test_get_webpage_http_404_error(self, mock_get_browser):
        """Test handling of HTTP 404 Not Found error"""
        from ncaa_stats_py.utls import _get_webpage

        # Mock browser and context
        mock_page = Mock()
        mock_response = Mock()
        mock_response.status = 404
        mock_page.goto.return_value = mock_response

        mock_context = Mock()
        mock_context.new_page.return_value = mock_page

        mock_browser = Mock()
        mock_get_browser.return_value = (mock_browser, mock_context)

        # Call function and expect ConnectionRefusedError
        with pytest.raises(ConnectionRefusedError, match="HTTP 404"):
            _get_webpage("https://example.com/not-found")

    @pytest.mark.unit
    @patch('ncaa_stats_py.utls._get_browser')
    def test_get_webpage_http_500_error(self, mock_get_browser):
        """Test handling of HTTP 500 Internal Server Error"""
        from ncaa_stats_py.utls import _get_webpage

        # Mock browser and context
        mock_page = Mock()
        mock_response = Mock()
        mock_response.status = 500
        mock_page.goto.return_value = mock_response

        mock_context = Mock()
        mock_context.new_page.return_value = mock_page

        mock_browser = Mock()
        mock_get_browser.return_value = (mock_browser, mock_context)

        # Call function and expect ConnectionError
        with pytest.raises(ConnectionError, match="HTTP 500"):
            _get_webpage("https://example.com/server-error")

    @pytest.mark.unit
    @patch('ncaa_stats_py.utls._get_browser')
    def test_get_webpage_success_200(self, mock_get_browser):
        """Test successful webpage retrieval with HTTP 200"""
        from ncaa_stats_py.utls import _get_webpage

        # Mock browser and context
        mock_page = Mock()
        mock_response = Mock()
        mock_response.status = 200
        mock_page.goto.return_value = mock_response
        mock_page.content.return_value = "<html><body>Success</body></html>"

        mock_context = Mock()
        mock_context.new_page.return_value = mock_page

        mock_browser = Mock()
        mock_get_browser.return_value = (mock_browser, mock_context)

        # Call function
        result = _get_webpage("https://example.com/page")

        # Assertions
        assert hasattr(result, 'text')
        assert "Success" in result.text
        assert hasattr(result, 'status_code')
        assert result.status_code == 200
