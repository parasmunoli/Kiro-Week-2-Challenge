"""Command-line interface for File Organization Bot."""
import sys
import argparse
from pathlib import Path
from typing import Optional

from .logger import setup_logger
from .categorizer import FileCategorizer
from .file_mover import FileMover
from .organizer import FileOrganizer, is_path_inside
from .watcher import FileWatcher


def get_default_downloads_path() -> Path:
    """
    Get the default Downloads folder path for the current platform.
    
    Returns:
        Path to the Downloads folder
    """
    # Works for Windows, macOS, and Linux
    downloads_path = Path.home() / "Downloads"
    
    # Verify it exists
    if not downloads_path.exists():
        raise FileNotFoundError(
            f"Default Downloads folder not found: {downloads_path}\n"
            "Please specify a custom path using --path"
        )
    
    return downloads_path


def run_watch_mode(args: argparse.Namespace) -> int:
    """
    Run the bot in watch mode (real-time monitoring).
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Setup logger
        log_file = Path(args.log_file) if args.log_file else None
        logger = setup_logger(log_file=log_file)
        
        # Get watch path
        watch_path = Path(args.path) if args.path else get_default_downloads_path()
        
        # Validate path exists
        if not watch_path.exists():
            print(f"Error: Path does not exist: {watch_path}", file=sys.stderr)
            return 1
        
        if not watch_path.is_dir():
            print(f"Error: Path is not a directory: {watch_path}", file=sys.stderr)
            return 1
        
        logger.info("=" * 60)
        logger.info("File Organization Bot - Watch Mode")
        logger.info("=" * 60)
        logger.info(f"Monitoring: {watch_path}")
        
        # Initialize components
        categorizer = FileCategorizer()
        file_mover = FileMover(logger)
        organizer = FileOrganizer(watch_path, categorizer, file_mover, logger)
        watcher = FileWatcher(watch_path, organizer, logger)
        
        # Start watching
        watcher.start()
        
        return 0
        
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def run_organize_mode(args: argparse.Namespace) -> int:
    """
    Run the bot in organize mode (one-time batch processing).
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Setup logger
        log_file = Path(args.log_file) if args.log_file else None
        logger = setup_logger(log_file=log_file)
        
        # Get organize path
        organize_path = Path(args.path) if args.path else get_default_downloads_path()
        
        # Validate path exists
        if not organize_path.exists():
            print(f"Error: Path does not exist: {organize_path}", file=sys.stderr)
            return 1
        
        if not organize_path.is_dir():
            print(f"Error: Path is not a directory: {organize_path}", file=sys.stderr)
            return 1
        
        logger.info("=" * 60)
        logger.info("File Organization Bot - Organize Mode")
        logger.info("=" * 60)
        logger.info(f"Organizing: {organize_path}")
        
        # Initialize components
        categorizer = FileCategorizer()
        file_mover = FileMover(logger)
        organizer = FileOrganizer(organize_path, categorizer, file_mover, logger)
        
        # Organize all files
        count = organizer.organize_all()
        
        logger.info("=" * 60)
        logger.info(f"Successfully organized {count} files")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main():
    """
    Main entry point for the CLI.
    Parses arguments and executes the appropriate mode.
    """
    parser = argparse.ArgumentParser(
        prog="file-organizer",
        description="Automatically organize files by type and date",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Watch Downloads folder in real-time
  file-organizer watch
  
  # Organize existing files once
  file-organizer organize
  
  # Watch a custom directory
  file-organizer watch --path /path/to/folder
  
  # Enable file logging
  file-organizer watch --log-file organizer.log
        """
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Watch command
    watch_parser = subparsers.add_parser(
        'watch',
        help='Monitor directory in real-time and organize new files automatically'
    )
    watch_parser.add_argument(
        '--path',
        type=str,
        help='Directory to monitor (default: ~/Downloads)'
    )
    watch_parser.add_argument(
        '--log-file',
        type=str,
        help='Enable file logging to specified path'
    )
    
    # Organize command
    organize_parser = subparsers.add_parser(
        'organize',
        help='Organize all existing files in directory once'
    )
    organize_parser.add_argument(
        '--path',
        type=str,
        help='Directory to organize (default: ~/Downloads)'
    )
    organize_parser.add_argument(
        '--log-file',
        type=str,
        help='Enable file logging to specified path'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute appropriate command
    if args.command == 'watch':
        sys.exit(run_watch_mode(args))
    elif args.command == 'organize':
        sys.exit(run_organize_mode(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
