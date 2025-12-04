"""
Example showing how to extend the categorizer with custom categories.

This demonstrates how you could add your own file type categories
beyond the default ones.
"""
from pathlib import Path
from file_organizer.categorizer import FileCategorizer
from file_organizer.file_mover import FileMover
from file_organizer.organizer import FileOrganizer
from file_organizer.logger import setup_logger


class CustomFileCategorizer(FileCategorizer):
    """Extended categorizer with custom categories."""
    
    def __init__(self):
        """Initialize with custom categories."""
        # Add custom categories
        self.CATEGORIES = {
            **FileCategorizer.CATEGORIES,  # Include default categories
            "Code": {"py", "js", "java", "cpp", "c", "h", "cs", "go", "rs"},
            "Data": {"csv", "json", "xml", "yaml", "yml", "sql"},
            "Ebooks": {"epub", "mobi", "azw", "azw3"},
        }
        
        # Rebuild the extension mapping
        self._extension_to_category = {}
        for category, extensions in self.CATEGORIES.items():
            for ext in extensions:
                self._extension_to_category[ext.lower()] = category


def main():
    """Organize files with custom categories."""
    
    logger = setup_logger(name="custom_example")
    directory = Path.home() / "Downloads"
    
    # Use custom categorizer
    categorizer = CustomFileCategorizer()
    file_mover = FileMover(logger)
    organizer = FileOrganizer(directory, categorizer, file_mover, logger)
    
    # Test the custom categories
    test_files = [
        "script.py",
        "data.csv",
        "book.epub",
        "photo.jpg",
    ]
    
    for filename in test_files:
        file_path = Path(filename)
        category = categorizer.get_category(file_path)
        logger.info(f"{filename} -> {category}")
    
    # Organize all files
    count = organizer.organize_all()
    logger.info(f"Organized {count} files with custom categories!")


if __name__ == "__main__":
    main()
