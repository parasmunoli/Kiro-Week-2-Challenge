"""File categorization based on extension."""
from pathlib import Path
from typing import Dict, Set


class FileCategorizer:
    """Categorizes files based on their extension."""
    
    # Extension to category mappings
    CATEGORIES: Dict[str, Set[str]] = {
        "Pictures": {"jpg", "jpeg", "png", "gif", "bmp", "svg", "webp"},
        "Documents": {"pdf", "doc", "docx", "txt", "rtf", "odt", "xls", "xlsx", "ppt", "pptx"},
        "Videos": {"mp4", "avi", "mkv", "mov", "wmv", "flv", "webm"},
        "Audio": {"mp3", "wav", "flac", "aac", "ogg", "m4a"},
        "Archives": {"zip", "rar", "tar", "gz", "7z", "bz2"},
    }
    
    def __init__(self):
        """Initialize the file categorizer."""
        # Create reverse mapping for faster lookup
        self._extension_to_category: Dict[str, str] = {}
        for category, extensions in self.CATEGORIES.items():
            for ext in extensions:
                self._extension_to_category[ext.lower()] = category
    
    def get_category(self, file_path: Path) -> str:
        """
        Determines the category for a given file based on its extension.
        
        Args:
            file_path: Path object representing the file
            
        Returns:
            Category name as string (Pictures, Documents, Videos, Audio, Archives, or Others)
        """
        # Get the file extension without the dot and normalize to lowercase
        extension = file_path.suffix.lstrip('.').lower()
        
        # Handle files without extensions
        if not extension:
            return "Others"
        
        # Look up the category, default to "Others" if not found
        return self._extension_to_category.get(extension, "Others")
