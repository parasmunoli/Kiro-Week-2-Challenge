"""
Basic usage example for File Organization Bot.

This script demonstrates how to use the bot programmatically
instead of through the CLI.
"""
from pathlib import Path
from file_organizer.categorizer import FileCategorizer
from file_organizer.file_mover import FileMover
from file_organizer.organizer import FileOrganizer
from file_organizer.logger import setup_logger


def main():
    """Organize files in a custom directory."""
    
    # Setup logging
    logger = setup_logger(name="example", log_file=Path("example.log"))
    
    # Specify the directory to organize
    directory_to_organize = Path.home() / "Downloads"
    
    logger.info(f"Organizing files in: {directory_to_organize}")
    
    # Initialize components
    categorizer = FileCategorizer()
    file_mover = FileMover(logger)
    organizer = FileOrganizer(directory_to_organize, categorizer, file_mover, logger)
    
    # Organize all files
    count = organizer.organize_all()
    
    logger.info(f"Successfully organized {count} files!")


if __name__ == "__main__":
    main()
