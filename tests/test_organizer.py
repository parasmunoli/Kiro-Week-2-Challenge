"""Unit tests for FileOrganizer."""
import pytest
import logging
from pathlib import Path
from file_organizer.categorizer import FileCategorizer
from file_organizer.file_mover import FileMover
from file_organizer.organizer import FileOrganizer


class TestFileOrganizer:
    """Test suite for FileOrganizer class."""
    
    def test_organizer_initialization(self, temp_dir):
        """Test that organizer initializes correctly."""
        logger = logging.getLogger("test")
        categorizer = FileCategorizer()
        mover = FileMover(logger)
        
        organizer = FileOrganizer(temp_dir, categorizer, mover, logger)
        
        assert organizer.base_path == temp_dir
        assert organizer.categorizer == categorizer
        assert organizer.file_mover == mover
    
    def test_organizer_invalid_path(self):
        """Test that organizer raises error for invalid path."""
        logger = logging.getLogger("test")
        categorizer = FileCategorizer()
        mover = FileMover(logger)
        
        with pytest.raises(ValueError, match="does not exist"):
            FileOrganizer(Path("/nonexistent/path"), categorizer, mover, logger)
    
    def test_organize_single_file(self, temp_dir):
        """Test organizing a single file."""
        logger = logging.getLogger("test")
        categorizer = FileCategorizer()
        mover = FileMover(logger)
        organizer = FileOrganizer(temp_dir, categorizer, mover, logger)
        
        # Create test file
        test_file = temp_dir / "test.pdf"
        test_file.write_text("test content")
        
        # Organize file
        result = organizer.organize_file(test_file)
        
        assert result is True
        assert not test_file.exists()  # File should be moved
        
        # Check file was moved to correct location
        documents_dir = temp_dir / "Documents"
        assert documents_dir.exists()
    
    def test_organize_all_files(self, test_files, temp_dir):
        """Test organizing all files in directory."""
        logger = logging.getLogger("test")
        categorizer = FileCategorizer()
        mover = FileMover(logger)
        organizer = FileOrganizer(temp_dir, categorizer, mover, logger)
        
        # Organize all files
        count = organizer.organize_all()
        
        assert count == len(test_files)
        
        # Verify files were moved
        for file_path in test_files.keys():
            assert not file_path.exists()
    
    def test_skip_hidden_files(self, temp_dir):
        """Test that hidden files are skipped."""
        logger = logging.getLogger("test")
        categorizer = FileCategorizer()
        mover = FileMover(logger)
        organizer = FileOrganizer(temp_dir, categorizer, mover, logger)
        
        # Create hidden file
        hidden_file = temp_dir / ".hidden.txt"
        hidden_file.write_text("hidden")
        
        # Try to organize
        result = organizer.organize_file(hidden_file)
        
        assert result is False
        assert hidden_file.exists()  # File should not be moved
    
    def test_skip_temporary_files(self, temp_dir):
        """Test that temporary files are skipped."""
        logger = logging.getLogger("test")
        categorizer = FileCategorizer()
        mover = FileMover(logger)
        organizer = FileOrganizer(temp_dir, categorizer, mover, logger)
        
        # Create temp files
        temp_file1 = temp_dir / "file.tmp"
        temp_file2 = temp_dir / "file.temp"
        temp_file1.write_text("temp")
        temp_file2.write_text("temp")
        
        # Try to organize
        assert organizer.organize_file(temp_file1) is False
        assert organizer.organize_file(temp_file2) is False
        
        assert temp_file1.exists()
        assert temp_file2.exists()
    
    def test_handle_missing_file(self, temp_dir):
        """Test handling of missing files."""
        logger = logging.getLogger("test")
        categorizer = FileCategorizer()
        mover = FileMover(logger)
        organizer = FileOrganizer(temp_dir, categorizer, mover, logger)
        
        # Try to organize non-existent file
        missing_file = temp_dir / "missing.pdf"
        result = organizer.organize_file(missing_file)
        
        assert result is False
