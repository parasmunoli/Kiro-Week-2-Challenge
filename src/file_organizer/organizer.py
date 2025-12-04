"""Core file organization logic."""
import os
import logging
import time
from pathlib import Path
from datetime import datetime
from typing import Optional

from .categorizer import FileCategorizer
from .file_mover import FileMover


def is_path_inside(child: Path, parent: Path) -> bool:
    """
    Check if child path is inside parent path (circular reference detection).
    
    Args:
        child: Potential child path
        parent: Potential parent path
        
    Returns:
        True if child is inside parent
    """
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


class FileOrganizer:
    """Coordinates file categorization and movement operations."""
    
    def __init__(
        self,
        base_path: Path,
        categorizer: FileCategorizer,
        file_mover: FileMover,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the file organizer.
        
        Args:
            base_path: Root directory to organize (e.g., Downloads folder)
            categorizer: FileCategorizer instance
            file_mover: FileMover instance
            logger: Logger instance for operation tracking
        """
        self.base_path = Path(base_path)
        self.categorizer = categorizer
        self.file_mover = file_mover
        self.logger = logger or logging.getLogger(__name__)
        
        # Validate base path exists
        if not self.base_path.exists():
            raise ValueError(f"Base path does not exist: {self.base_path}")
        if not self.base_path.is_dir():
            raise ValueError(f"Base path is not a directory: {self.base_path}")
    
    def _get_file_date(self, file_path: Path) -> datetime:
        """
        Extract file modification date.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Datetime object representing file modification time
        """
        timestamp = os.path.getmtime(file_path)
        return datetime.fromtimestamp(timestamp)
    
    def _should_process_file(self, file_path: Path) -> bool:
        """
        Determine if a file should be processed.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file should be processed, False otherwise
        """
        # Skip if not a file
        if not file_path.is_file():
            return False
        
        # Skip hidden files (starting with .)
        if file_path.name.startswith('.'):
            return False
        
        # Skip if it's a symlink
        if file_path.is_symlink():
            self.logger.debug(f"Skipping symlink: {file_path}")
            return False
        
        # Skip temporary files
        if file_path.name.endswith('.tmp') or file_path.name.endswith('.temp'):
            return False
        
        return True
    
    def organize_file(self, file_path: Path, max_retries: int = 3) -> bool:
        """
        Organizes a single file into the appropriate category/date folder.
        
        Args:
            file_path: Path to the file to organize
            max_retries: Maximum number of retry attempts for locked files
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate file should be processed
            if not self._should_process_file(file_path):
                return False
            
            # Check if file still exists (may have been moved by another process)
            if not file_path.exists():
                self.logger.warning(f"File no longer exists: {file_path}")
                return False
            
            # Determine category
            category = self.categorizer.get_category(file_path)
            self.logger.info(f"Detected file: '{file_path.name}' -> Category: {category}")
            
            # Get file date
            file_date = self._get_file_date(file_path)
            
            # Move the file with retry logic for locked files
            for attempt in range(max_retries):
                try:
                    self.file_mover.move_file(file_path, self.base_path, category, file_date)
                    return True
                except PermissionError as e:
                    if attempt < max_retries - 1:
                        # File might be locked, wait and retry with exponential backoff
                        wait_time = 2 ** attempt  # 1s, 2s, 4s
                        self.logger.warning(
                            f"File locked, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries}): {file_path}"
                        )
                        time.sleep(wait_time)
                    else:
                        self.logger.error(f"Permission denied after {max_retries} attempts for '{file_path}': {e}")
                        return False
                except OSError as e:
                    # Handle disk space and other OS errors (don't retry these)
                    self.logger.error(f"Failed to move '{file_path}': {e}")
                    return False
                
        except Exception as e:
            self.logger.error(f"Unexpected error organizing '{file_path}': {e}")
            return False
    
    def organize_all(self) -> int:
        """
        Organizes all files in the base directory.
        
        Returns:
            Number of files successfully organized
        """
        self.logger.info(f"Starting organization of: {self.base_path}")
        
        count = 0
        files = [f for f in self.base_path.iterdir() if f.is_file()]
        
        self.logger.info(f"Found {len(files)} files to process")
        
        for file_path in files:
            if self.organize_file(file_path):
                count += 1
        
        self.logger.info(f"Organization complete. Processed {count} files.")
        return count
