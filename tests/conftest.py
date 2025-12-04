"""Shared pytest fixtures for File Organization Bot tests."""
import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def test_files(temp_dir):
    """Create test files in the temporary directory."""
    files = {
        'test.pdf': 'Documents',
        'photo.jpg': 'Pictures',
        'video.mp4': 'Videos',
        'song.mp3': 'Audio',
        'archive.zip': 'Archives',
        'unknown.xyz': 'Others',
    }
    
    created_files = {}
    for filename, expected_category in files.items():
        file_path = temp_dir / filename
        file_path.write_text(f"Test content for {filename}")
        created_files[file_path] = expected_category
    
    return created_files


@pytest.fixture
def sample_date():
    """Return a sample datetime for testing."""
    return datetime(2025, 12, 4, 10, 30, 0)
