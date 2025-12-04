"""Unit tests for FileCategorizer."""
import pytest
from pathlib import Path
from file_organizer.categorizer import FileCategorizer


class TestFileCategorizer:
    """Test suite for FileCategorizer class."""
    
    def test_categorize_image_files(self):
        """Test that image extensions are categorized as Pictures."""
        categorizer = FileCategorizer()
        
        image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp']
        for ext in image_extensions:
            file_path = Path(f"test.{ext}")
            assert categorizer.get_category(file_path) == "Pictures"
    
    def test_categorize_document_files(self):
        """Test that document extensions are categorized as Documents."""
        categorizer = FileCategorizer()
        
        doc_extensions = ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt', 'xls', 'xlsx', 'ppt', 'pptx']
        for ext in doc_extensions:
            file_path = Path(f"test.{ext}")
            assert categorizer.get_category(file_path) == "Documents"
    
    def test_categorize_video_files(self):
        """Test that video extensions are categorized as Videos."""
        categorizer = FileCategorizer()
        
        video_extensions = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm']
        for ext in video_extensions:
            file_path = Path(f"test.{ext}")
            assert categorizer.get_category(file_path) == "Videos"
    
    def test_categorize_audio_files(self):
        """Test that audio extensions are categorized as Audio."""
        categorizer = FileCategorizer()
        
        audio_extensions = ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a']
        for ext in audio_extensions:
            file_path = Path(f"test.{ext}")
            assert categorizer.get_category(file_path) == "Audio"
    
    def test_categorize_archive_files(self):
        """Test that archive extensions are categorized as Archives."""
        categorizer = FileCategorizer()
        
        archive_extensions = ['zip', 'rar', 'tar', 'gz', '7z', 'bz2']
        for ext in archive_extensions:
            file_path = Path(f"test.{ext}")
            assert categorizer.get_category(file_path) == "Archives"
    
    def test_categorize_unknown_extension(self):
        """Test that unknown extensions are categorized as Others."""
        categorizer = FileCategorizer()
        
        file_path = Path("test.xyz")
        assert categorizer.get_category(file_path) == "Others"
    
    def test_categorize_no_extension(self):
        """Test that files without extensions are categorized as Others."""
        categorizer = FileCategorizer()
        
        file_path = Path("README")
        assert categorizer.get_category(file_path) == "Others"
    
    def test_case_insensitive_categorization(self):
        """Test that extension matching is case-insensitive."""
        categorizer = FileCategorizer()
        
        # Test uppercase
        assert categorizer.get_category(Path("test.PDF")) == "Documents"
        assert categorizer.get_category(Path("test.JPG")) == "Pictures"
        
        # Test mixed case
        assert categorizer.get_category(Path("test.PdF")) == "Documents"
        assert categorizer.get_category(Path("test.JpG")) == "Pictures"
