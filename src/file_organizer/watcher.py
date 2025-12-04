"""Real-time file system monitoring."""
import time
import logging
from pathlib import Path
from typing import Optional
from threading import Timer

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from .organizer import FileOrganizer


class FileEventHandler(FileSystemEventHandler):
    """Handles file system events for the file organizer."""
    
    def __init__(self, organizer: FileOrganizer, logger: logging.Logger, debounce_seconds: float = 1.0):
        """
        Initialize the event handler.
        
        Args:
            organizer: FileOrganizer instance to process files
            logger: Logger instance
            debounce_seconds: Delay before processing files to ensure writes are complete
        """
        super().__init__()
        self.organizer = organizer
        self.logger = logger
        self.debounce_seconds = debounce_seconds
        self._pending_timers = {}
    
    def on_created(self, event):
        """
        Handle file creation events.
        
        Args:
            event: File system event
        """
        # Ignore directory creation events
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Cancel any existing timer for this file
        if file_path in self._pending_timers:
            self._pending_timers[file_path].cancel()
        
        # Schedule processing after debounce delay
        timer = Timer(self.debounce_seconds, self._process_file, args=[file_path])
        self._pending_timers[file_path] = timer
        timer.start()
    
    def _process_file(self, file_path: Path):
        """
        Process a file after debounce delay.
        
        Args:
            file_path: Path to the file to process
        """
        try:
            self.organizer.organize_file(file_path)
        finally:
            # Clean up timer reference
            if file_path in self._pending_timers:
                del self._pending_timers[file_path]


class FileWatcher:
    """Monitors a directory for new files and organizes them automatically."""
    
    def __init__(
        self,
        watch_path: Path,
        organizer: FileOrganizer,
        logger: Optional[logging.Logger] = None,
        debounce_seconds: float = 1.0
    ):
        """
        Initialize the file watcher.
        
        Args:
            watch_path: Directory to monitor
            organizer: FileOrganizer instance to handle detected files
            logger: Logger instance
            debounce_seconds: Delay before processing files
        """
        self.watch_path = Path(watch_path)
        self.organizer = organizer
        self.logger = logger or logging.getLogger(__name__)
        self.debounce_seconds = debounce_seconds
        
        # Validate watch path
        if not self.watch_path.exists():
            raise ValueError(f"Watch path does not exist: {self.watch_path}")
        if not self.watch_path.is_dir():
            raise ValueError(f"Watch path is not a directory: {self.watch_path}")
        
        # Create event handler and observer
        self.event_handler = FileEventHandler(organizer, self.logger, debounce_seconds)
        self.observer = Observer()
    
    def start(self) -> None:
        """
        Starts monitoring the directory for file system events.
        Blocks until stopped with Ctrl+C or stop() is called.
        """
        self.logger.info(f"Starting file watcher on: {self.watch_path}")
        self.logger.info("Press Ctrl+C to stop watching...")
        
        # Schedule the observer
        self.observer.schedule(self.event_handler, str(self.watch_path), recursive=False)
        self.observer.start()
        
        try:
            # Keep the main thread alive
            while self.observer.is_alive():
                self.observer.join(timeout=1)
        except KeyboardInterrupt:
            self.logger.info("Received stop signal")
            self.stop()
    
    def stop(self) -> None:
        """
        Stops monitoring and releases resources.
        """
        self.logger.info("Stopping file watcher...")
        self.observer.stop()
        self.observer.join()
        self.logger.info("File watcher stopped")
