"""Unit tests for FileMover."""
import pytest
import logging
from pathlib import Path
from datetime import datetime
from file_organizer.file_mover import FileMover


class TestFileMover:
    """Test suite for FileMover class."""
    
    def test_create_destination_path_structure(self, temp_dir, sample_date):
        """Test that destination path follows Category/YYYY/MMM format."""
        logger = logging.getLogger("test")
        mover = FileMover(logger)
        
        dest_path = mover.create_destination_path(temp_dir, "Pictures", sample_date)
        
        # Check path structure (dest_path is the full directory: base/Category/YYYY/MMM)
        assert dest_path.name == "Dec"  # Month (last component)
        assert dest_path.parent.name == "2025"  # Year
        assert dest_path.parent.parent.name == "Pictures"  # Category
        
        # Check directory was created
        assert dest_path.exists()
        assert dest_path.is_dir()
    
    def test_create_destination_path_different_months(self, temp_dir):
        """Test path creation for different months."""
        logger = logging.getLogger("test")
        mover = FileMover(logger)
        
        test_dates = [
            (datetime(2025, 1, 15), "Jan"),
            (datetime(2025, 6, 20), "Jun"),
            (datetime(2025, 12, 31), "Dec"),
        ]
        
        for date, expected_month in test_dates:
            dest_path = mover.create_destination_path(temp_dir, "Documents", date)
            assert dest_path.name == expected_month  # dest_path is the full directory
    
    def test_handle_duplicate_no_conflict(self, temp_dir):
        """Test that handle_duplicate returns original path when no conflict."""
        logger = logging.getLogger("test")
        mover = FileMover(logger)
        
        destination = temp_dir / "test.pdf"
        result = mover.handle_duplicate(destination)
        
        assert result == destination
    
    def test_handle_duplicate_with_conflict(self, temp_dir):
        """Test that handle_duplicate appends numeric suffix for conflicts."""
        logger = logging.getLogger("test")
        mover = FileMover(logger)
        
        # Create existing file
        existing = temp_dir / "test.pdf"
        existing.write_text("existing")
        
        # Test duplicate handling
        destination = temp_dir / "test.pdf"
        result = mover.handle_duplicate(destination)
        
        assert result == temp_dir / "test(1).pdf"
        assert result.suffix == ".pdf"  # Extension preserved
    
    def test_handle_duplicate_multiple_conflicts(self, temp_dir):
        """Test handling multiple duplicates."""
        logger = logging.getLogger("test")
        mover = FileMover(logger)
        
        # Create existing files
        (temp_dir / "test.pdf").write_text("1")
        (temp_dir / "test(1).pdf").write_text("2")
        (temp_dir / "test(2).pdf").write_text("3")
        
        # Test duplicate handling
        destination = temp_dir / "test.pdf"
        result = mover.handle_duplicate(destination)
        
        assert result == temp_dir / "test(3).pdf"
    
    def test_handle_duplicate_preserves_extension(self, temp_dir):
        """Test that file extension is preserved in duplicate names."""
        logger = logging.getLogger("test")
        mover = FileMover(logger)
        
        # Test with various extensions
        # Note: Path.suffix only gets the last extension, so file.tar.gz becomes file.tar(1).gz
        # This is acceptable behavior for our use case
        test_cases = [
            ("file.tar.gz", "file.tar(1).gz"),  # Only last extension preserved
            ("document.backup.pdf", "document.backup(1).pdf"),  # Only last extension preserved
            ("image.jpg", "image(1).jpg"),
        ]
        
        for original, expected in test_cases:
            (temp_dir / original).write_text("test")
            destination = temp_dir / original
            result = mover.handle_duplicate(destination)
            assert result.name == expected
            # Cleanup for next iteration
            (temp_dir / original).unlink()
    
    def test_move_file_success(self, temp_dir, sample_date):
        """Test successful file move operation."""
        logger = logging.getLogger("test")
        mover = FileMover(logger)
        
        # Create source file
        source = temp_dir / "test.pdf"
        source.write_text("test content")
        
        # Move file
        result = mover.move_file(source, temp_dir, "Documents", sample_date)
        
        # Verify file was moved
        assert not source.exists()
        assert result.exists()
        assert result.read_text() == "test content"
        
        # Verify path structure
        assert "Documents" in str(result)
        assert "2025" in str(result)
        assert "Dec" in str(result)
