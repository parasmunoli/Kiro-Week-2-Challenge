# Design Document

## Overview

The File Organization Bot is a Python-based automation tool that monitors a Downloads folder and automatically organizes files into a structured directory hierarchy based on file type and date. The system uses the `watchdog` library for real-time file system monitoring, `pathlib` for cross-platform path handling, and implements a modular architecture separating concerns between file watching, categorization, and file operations.

The bot operates in two modes: **watch mode** for continuous real-time monitoring, and **organize mode** for one-time batch processing. All file operations are logged to provide transparency and enable troubleshooting.

## Architecture

The system follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                     CLI Interface                        │
│              (Argument parsing & control)                │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼────────┐    ┌────────▼────────┐
│  Watch Mode     │    │  Organize Mode  │
│  (Real-time)    │    │  (One-time)     │
└────────┬────────┘    └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │   File Organizer      │
         │   (Core Logic)        │
         └───────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼────────┐    ┌────────▼────────┐
│  Categorizer    │    │  File Mover     │
│  (Type detect)  │    │  (Operations)   │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │    Logger System      │
         │  (Console + File)     │
         └───────────────────────┘
```

### Component Responsibilities

1. **CLI Interface**: Parses command-line arguments and initializes the appropriate mode
2. **Watch Mode**: Uses `watchdog` to monitor file system events in real-time
3. **Organize Mode**: Scans directory once and processes all existing files
4. **File Organizer**: Coordinates categorization and file movement operations
5. **Categorizer**: Determines file type category based on extension
6. **File Mover**: Handles physical file operations with duplicate detection
7. **Logger System**: Provides consistent logging across all components

## Components and Interfaces

### 1. FileCategorizer

**Purpose**: Determines the category of a file based on its extension.

**Interface**:
```python
class FileCategorizer:
    def get_category(self, file_path: Path) -> str:
        """
        Determines the category for a given file.
        
        Args:
            file_path: Path object representing the file
            
        Returns:
            Category name as string (Pictures, Documents, Videos, etc.)
        """
```

**Category Mappings**:
- Pictures: jpg, jpeg, png, gif, bmp, svg, webp
- Documents: pdf, doc, docx, txt, rtf, odt, xls, xlsx, ppt, pptx
- Videos: mp4, avi, mkv, mov, wmv, flv, webm
- Audio: mp3, wav, flac, aac, ogg, m4a
- Archives: zip, rar, tar, gz, 7z, bz2
- Others: all unmatched extensions

### 2. FileOrganizer

**Purpose**: Core orchestration component that coordinates file categorization and movement.

**Interface**:
```python
class FileOrganizer:
    def __init__(self, base_path: Path, categorizer: FileCategorizer, logger: logging.Logger):
        """
        Initializes the file organizer.
        
        Args:
            base_path: Root directory to organize (e.g., Downloads folder)
            categorizer: FileCategorizer instance
            logger: Logger instance for operation tracking
        """
    
    def organize_file(self, file_path: Path) -> bool:
        """
        Organizes a single file into the appropriate category/date folder.
        
        Args:
            file_path: Path to the file to organize
            
        Returns:
            True if successful, False otherwise
        """
    
    def organize_all(self) -> int:
        """
        Organizes all files in the base directory.
        
        Returns:
            Number of files successfully organized
        """
```

### 3. FileMover

**Purpose**: Handles physical file operations including duplicate detection and renaming.

**Interface**:
```python
class FileMover:
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
        """
    
    def create_destination_path(self, base_dir: Path, category: str, file_date: datetime) -> Path:
        """
        Creates the destination directory structure: Category/YYYY/MMM
        
        Args:
            base_dir: Base directory
            category: File category
            file_date: Date for folder structure
            
        Returns:
            Created directory path
        """
    
    def handle_duplicate(self, destination: Path) -> Path:
        """
        Handles duplicate filenames by appending numeric suffix.
        
        Args:
            destination: Intended destination path
            
        Returns:
            Available path with suffix if needed (e.g., file(1).pdf)
        """
```

### 4. FileWatcher

**Purpose**: Monitors the Downloads folder for new files in real-time using `watchdog`.

**Interface**:
```python
class FileWatcher:
    def __init__(self, watch_path: Path, organizer: FileOrganizer, logger: logging.Logger):
        """
        Initializes the file watcher.
        
        Args:
            watch_path: Directory to monitor
            organizer: FileOrganizer instance to handle detected files
            logger: Logger instance
        """
    
    def start(self) -> None:
        """
        Starts monitoring the directory for file system events.
        Blocks until stopped.
        """
    
    def stop(self) -> None:
        """
        Stops monitoring and releases resources.
        """
```

### 5. CLI Module

**Purpose**: Provides command-line interface for user interaction.

**Interface**:
```python
def main():
    """
    Main entry point. Parses arguments and executes appropriate mode.
    
    Commands:
        watch [--path PATH] [--log-file FILE]: Start real-time monitoring
        organize [--path PATH] [--log-file FILE]: One-time organization
        --help: Display usage information
    """
```

## Data Models

### File Metadata

```python
@dataclass
class FileMetadata:
    """Represents metadata about a file being organized."""
    path: Path
    category: str
    creation_date: datetime
    size: int
    extension: str
```

### Configuration

```python
@dataclass
class OrganizerConfig:
    """Configuration for the file organizer."""
    watch_path: Path
    enable_file_logging: bool = False
    log_file_path: Optional[Path] = None
    delay_seconds: float = 1.0  # Delay before processing new files
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Extension categorization correctness

*For any* file with a recognized extension, the categorizer should map it to exactly one correct category according to the defined extension mappings (images→Pictures, documents→Documents, videos→Videos, audio→Audio, archives→Archives), and any file with an unrecognized extension should be categorized as Others.

**Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7**

### Property 2: Date-based path structure correctness

*For any* file with a valid date and category, the generated destination path should follow the format `Category/YYYY/MMM` where YYYY is the four-digit year and MMM is the three-letter month abbreviation, and all necessary directories should be created if they don't exist.

**Validates: Requirements 2.2, 2.3, 2.4**

### Property 3: File relocation completeness

*For any* file that is successfully organized, the file should exist at the destination path and should not exist at the source path after the operation completes.

**Validates: Requirements 2.5**

### Property 4: Duplicate filename handling

*For any* file being moved to a destination where a file with the same name already exists, the system should append a numeric suffix in the format `filename(N).ext` where N is the smallest positive integer that results in a unique filename, and the file extension should remain unchanged.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4**

### Property 5: Operation logging completeness

*For any* file organization operation (detection, successful move, duplicate rename, or error), the logger should produce a log entry containing relevant information about the operation (file name, category, paths, or error details as appropriate).

**Validates: Requirements 4.2, 4.3, 4.4, 4.5**

### Property 6: Cross-platform path handling

*For any* file path operation, the system should use pathlib.Path objects and should not contain hardcoded platform-specific path separators (like `\` or `/`), ensuring paths work correctly across Windows, macOS, and Linux.

**Validates: Requirements 6.1**

## Error Handling

### File Operation Errors

**Permission Errors**: When the bot lacks permissions to read a source file or write to a destination:
- Log the error with file path and permission details
- Skip the file and continue processing other files
- Do not crash or terminate the bot

**File Not Found**: When a file disappears between detection and processing:
- Log a warning that the file is no longer available
- Continue processing other files
- Common in watch mode when files are quickly moved by other processes

**Disk Space Errors**: When insufficient disk space prevents file movement:
- Log the error with space requirements
- Leave the file in its original location
- Alert the user through logging

**File Lock Errors**: When a file is in use by another process:
- Implement retry logic with exponential backoff (3 attempts)
- Log each retry attempt
- If all retries fail, log error and skip the file

### Path Resolution Errors

**Invalid Paths**: When provided paths don't exist or are invalid:
- Validate paths at startup before beginning operations
- Provide clear error messages indicating which path is invalid
- Exit gracefully with non-zero status code

**Circular References**: When destination path is within source path:
- Detect this condition at startup
- Prevent operation to avoid infinite loops
- Exit with clear error message

### Configuration Errors

**Missing Dependencies**: When required libraries are not installed:
- Catch ImportError at module level
- Provide clear installation instructions in error message
- Exit gracefully

**Invalid Arguments**: When CLI arguments are malformed:
- Use argparse validation to catch errors early
- Display usage help automatically
- Exit with appropriate error code

## Testing Strategy

The File Organization Bot will employ a dual testing approach combining unit tests and property-based tests to ensure comprehensive correctness validation.

### Unit Testing Approach

Unit tests will verify specific examples and integration points:

1. **Categorizer Tests**:
   - Test specific extension mappings (e.g., `.pdf` → Documents)
   - Test case-insensitive extension handling (`.PDF` and `.pdf`)
   - Test files without extensions

2. **Path Generation Tests**:
   - Test specific date formatting (e.g., December 2025 → "Dec")
   - Test path creation with specific categories and dates
   - Test edge cases like January 1st and December 31st

3. **Duplicate Handling Tests**:
   - Test renaming with specific examples (file.pdf → file(1).pdf)
   - Test multiple duplicates (file.pdf, file(1).pdf → file(2).pdf)
   - Test files with multiple dots (file.backup.tar.gz)

4. **CLI Integration Tests**:
   - Test help command output
   - Test argument parsing for watch and organize modes
   - Test custom path and log file arguments

5. **Error Handling Tests**:
   - Test behavior with permission errors (using mocked file operations)
   - Test behavior with missing files
   - Test behavior with invalid paths

### Property-Based Testing Approach

Property-based tests will verify universal correctness properties across many randomly generated inputs using the **Hypothesis** library for Python.

**Configuration**: Each property-based test will run a minimum of 100 iterations to ensure thorough coverage of the input space.

**Test Tagging**: Each property-based test must include a comment explicitly referencing the correctness property from this design document using the format: `# Feature: file-organizer-bot, Property N: <property text>`

**Key Property Tests**:

1. **Property 1 Test - Extension Categorization**:
   - Generate random filenames with various extensions
   - Verify each extension maps to the correct category
   - Verify unknown extensions map to "Others"
   - **Tag**: `# Feature: file-organizer-bot, Property 1: Extension categorization correctness`

2. **Property 2 Test - Path Structure**:
   - Generate random dates and categories
   - Verify generated paths match `Category/YYYY/MMM` format
   - Verify month abbreviations are correct
   - **Tag**: `# Feature: file-organizer-bot, Property 2: Date-based path structure correctness`

3. **Property 3 Test - File Relocation**:
   - Generate random files in a test directory
   - Organize them and verify they exist at destination
   - Verify they no longer exist at source
   - **Tag**: `# Feature: file-organizer-bot, Property 3: File relocation completeness`

4. **Property 4 Test - Duplicate Handling**:
   - Generate random filenames and create duplicates
   - Verify numeric suffixes are applied correctly
   - Verify extensions are preserved
   - Verify no files are overwritten
   - **Tag**: `# Feature: file-organizer-bot, Property 4: Duplicate filename handling`

5. **Property 5 Test - Logging**:
   - Perform random file operations
   - Verify each operation produces appropriate log entries
   - Verify log entries contain required information
   - **Tag**: `# Feature: file-organizer-bot, Property 5: Operation logging completeness`

6. **Property 6 Test - Cross-Platform Paths**:
   - Generate random path operations
   - Verify all paths use pathlib.Path
   - Verify no hardcoded separators exist in path strings
   - **Tag**: `# Feature: file-organizer-bot, Property 6: Cross-platform path handling`

### Test Organization

Tests will be organized in a `tests/` directory with the following structure:

```
tests/
├── test_categorizer.py          # Unit tests for FileCategorizer
├── test_file_mover.py            # Unit tests for FileMover
├── test_organizer.py             # Unit tests for FileOrganizer
├── test_cli.py                   # Unit tests for CLI interface
├── test_properties.py            # Property-based tests for all properties
└── conftest.py                   # Shared pytest fixtures
```

### Testing Tools

- **pytest**: Primary test runner
- **hypothesis**: Property-based testing library
- **pytest-cov**: Code coverage reporting
- **tempfile**: Creating temporary test directories
- **unittest.mock**: Mocking file system operations for error scenarios

## Implementation Notes

### Cross-Platform Considerations

1. **Path Handling**: Always use `pathlib.Path` for path operations. Never use string concatenation with `/` or `\`.

2. **Downloads Folder Location**:
   - Windows: `Path.home() / "Downloads"`
   - macOS: `Path.home() / "Downloads"`
   - Linux: `Path.home() / "Downloads"` (or check XDG_DOWNLOAD_DIR)

3. **File Timestamps**: Use `os.path.getmtime()` for modification time, which works consistently across platforms.

4. **Case Sensitivity**: File systems vary (Windows is case-insensitive, Linux is case-sensitive). Always normalize extensions to lowercase for comparison.

### Performance Considerations

1. **Watch Mode Debouncing**: Implement a small delay (1 second) after file detection before processing to ensure file writes are complete.

2. **Batch Processing**: In organize mode, process files in batches to provide progress feedback for large directories.

3. **File Size Checks**: For very large files, consider adding progress indicators or async operations.

### Security Considerations

1. **Path Traversal**: Validate that destination paths don't escape the intended directory structure.

2. **Symlink Handling**: Decide whether to follow symlinks or skip them (recommend skipping to avoid loops).

3. **Hidden Files**: Decide whether to process hidden files (files starting with `.` on Unix systems).

### Extensibility Points

1. **Custom Categories**: Design the categorizer to easily accept custom category definitions via configuration file.

2. **Naming Strategies**: Allow different duplicate naming strategies (suffix, prefix, timestamp).

3. **Filters**: Support excluding certain file types or patterns from organization.

4. **Plugins**: Consider a plugin architecture for custom organization rules.

## Dependencies

- **Python**: 3.8 or higher (for pathlib and type hints)
- **watchdog**: 2.1.0+ (file system monitoring)
- **hypothesis**: 6.0.0+ (property-based testing)
- **pytest**: 7.0.0+ (test runner)
- **pytest-cov**: 4.0.0+ (coverage reporting)

## Deployment

The bot will be distributed as:

1. **Python Package**: Installable via pip with entry point for CLI
2. **Standalone Script**: Single-file version for simple deployment
3. **GitHub Repository**: Source code with full documentation

### Installation Steps

```bash
# Clone repository
git clone https://github.com/username/file-organizer-bot.git
cd file-organizer-bot

# Install dependencies
pip install -r requirements.txt

# Run the bot
python file_organizer.py watch
```

### Configuration

Optional configuration file `.file-organizer-config.json`:

```json
{
  "watch_path": "/path/to/downloads",
  "categories": {
    "Pictures": ["jpg", "png", "gif"],
    "Documents": ["pdf", "docx", "txt"]
  },
  "enable_file_logging": true,
  "log_file_path": "organizer.log"
}
```
