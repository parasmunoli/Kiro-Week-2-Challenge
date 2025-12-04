"""File moving operations with duplicate handling."""
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional


class FileMover:
    """Handles file movement operations with duplicate detection and date-based organization."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the file mover.
        
        Args:
            logger: Logger instance for operation tracking
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def create_destination_path(self, base_dir: Path, category: str, file_date: datetime) -> Path:
        """
        Creates the destination directory structure: Category/YYYY/MMM
        
        Args:
            base_dir: Base directory for organization
            category: File category (Pictures, Documents, etc.)
            file_date: Date to use for folder structure
            
        Returns:
            Created directory path
        """
        # Format: Category/YYYY/MMM (e.g., Pictures/2025/Dec)
        year = file_date.strftime("%Y")
        month = file_date.strftime("%b")  # Three-letter month abbreviation
        
        destination_dir = base_dir / category / year / month
        
        # Create all necessary directories
        destination_dir.mkdir(parents=True, exist_ok=True)
        
        return destination_dir
    
    def handle_duplicate(self, destination: Path) -> Path:
        """
        Handles duplicate filenames by appending numeric suffix.
        
        Args:
            destination: Intended destination path
            
        Returns:
            Available path with suffix if needed (e.g., file(1).pdf)
        """
        if not destination.exists():
            return destination
        
        # Extract filename parts
        stem = destination.stem  # filename without extension
        suffix = destination.suffix  # extension including the dot
        parent = destination.parent
        
        # Find the next available number
        counter = 1
        while True:
            new_name = f"{stem}({counter}){suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
    
    def move_file(self, source: Path, destination_dir: Path, category: str, file_date: datetime) -> Path:
        """
        Moves a file to the destination with date-based folder structure.
        
        Args:
            source: Source file path
            destination_dir: Base destination directory
            category: File category (Pictures, Documents, etc.)
            file_date: Date to use for folder structure
            
        Returns:
            Final destination path where file was moved
            
        Raises:
            OSError: If file operation fails
        """
        # Create the destination directory structure
        dest_folder = self.create_destination_path(destination_dir, category, file_date)
        
        # Determine final destination path
        intended_destination = dest_folder / source.name
        final_destination = self.handle_duplicate(intended_destination)
        
        # Log if we had to rename due to duplicate
        if final_destination != intended_destination:
            self.logger.info(
                f"Duplicate detected: '{source.name}' renamed to '{final_destination.name}'"
            )
        
        # Move the file
        shutil.move(str(source), str(final_destination))
        
        self.logger.info(f"Moved: '{source}' -> '{final_destination}'")
        
        return final_destination
