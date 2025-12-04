# Implementation Plan

- [x] 1. Set up project structure and dependencies


  - Create project directory structure with src/, tests/, and docs/ folders
  - Create requirements.txt with watchdog, hypothesis, pytest, and pytest-cov
  - Create setup.py or pyproject.toml for package configuration
  - Create .gitignore for Python projects
  - _Requirements: 8.5_

- [x] 2. Implement FileCategorizer component


  - Create FileCategorizer class with extension-to-category mappings
  - Implement get_category() method with case-insensitive extension matching
  - Handle files without extensions (categorize as Others)
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

- [ ]* 2.1 Write property test for extension categorization
  - **Property 1: Extension categorization correctness**
  - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7**

- [ ]* 2.2 Write unit tests for FileCategorizer
  - Test specific extension mappings (.pdf → Documents, .jpg → Pictures)
  - Test case-insensitive handling (.PDF and .pdf)
  - Test files without extensions
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

- [x] 3. Implement FileMover component


  - Create FileMover class with path generation logic
  - Implement create_destination_path() to generate Category/YYYY/MMM structure
  - Implement handle_duplicate() to append numeric suffixes for duplicate filenames
  - Implement move_file() to orchestrate directory creation and file movement
  - _Requirements: 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4_

- [ ]* 3.1 Write property test for date-based path structure
  - **Property 2: Date-based path structure correctness**
  - **Validates: Requirements 2.2, 2.3, 2.4**

- [ ]* 3.2 Write property test for duplicate filename handling
  - **Property 4: Duplicate filename handling**
  - **Validates: Requirements 3.1, 3.2, 3.3, 3.4**

- [ ]* 3.3 Write unit tests for FileMover
  - Test path generation with specific dates (December 2025 → "Dec")
  - Test duplicate renaming (file.pdf → file(1).pdf → file(2).pdf)
  - Test extension preservation in duplicate names
  - Test files with multiple dots (file.backup.tar.gz)
  - _Requirements: 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4_

- [x] 4. Implement logging system


  - Configure Python logging with console handler
  - Add optional file handler when log file path is provided
  - Create log formatters with timestamps and log levels
  - Implement logging for file detection, moves, duplicates, and errors
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [ ]* 4.1 Write property test for operation logging
  - **Property 5: Operation logging completeness**
  - **Validates: Requirements 4.2, 4.3, 4.4, 4.5**

- [ ]* 4.2 Write unit tests for logging
  - Test console logging is initialized
  - Test file logging when enabled
  - Test log messages contain expected information
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [x] 5. Implement FileOrganizer core component


  - Create FileOrganizer class that coordinates categorizer and mover
  - Implement organize_file() to process a single file (categorize, determine date, move)
  - Implement organize_all() to scan and process all files in a directory
  - Add error handling for permission errors, missing files, and disk space issues
  - Extract file modification date using os.path.getmtime()
  - _Requirements: 2.1, 2.5, 3.1_

- [ ]* 5.1 Write property test for file relocation
  - **Property 3: File relocation completeness**
  - **Validates: Requirements 2.5**

- [ ]* 5.2 Write unit tests for FileOrganizer
  - Test organize_file() with various file types
  - Test organize_all() processes multiple files
  - Test error handling for permission errors
  - Test error handling for missing files
  - _Requirements: 2.1, 2.5_

- [x] 6. Implement FileWatcher for real-time monitoring


  - Create FileWatcher class using watchdog library
  - Implement event handler for file creation events
  - Add debouncing logic (1 second delay) to ensure file writes are complete
  - Implement start() method to begin monitoring
  - Implement stop() method for graceful shutdown
  - Filter out directory events and temporary files
  - _Requirements: 5.1, 5.2, 5.4_

- [ ]* 6.1 Write unit tests for FileWatcher
  - Test watch mode detects new files
  - Test debouncing delays processing appropriately
  - Test graceful shutdown releases resources
  - _Requirements: 5.1, 5.2, 5.4_

- [x] 7. Implement CLI interface


  - Create main() function with argparse for command-line argument parsing
  - Add 'watch' subcommand to start real-time monitoring mode
  - Add 'organize' subcommand for one-time batch processing
  - Add --path argument for custom directory (default to Downloads folder)
  - Add --log-file argument to enable file-based logging
  - Add --help to display usage instructions
  - Implement cross-platform Downloads folder detection (Path.home() / "Downloads")
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 6.2_

- [ ]* 7.1 Write property test for cross-platform path handling
  - **Property 6: Cross-platform path handling**
  - **Validates: Requirements 6.1**

- [ ]* 7.2 Write unit tests for CLI
  - Test 'watch' command starts watch mode
  - Test 'organize' command runs batch processing
  - Test --help displays usage information
  - Test --path argument uses custom directory
  - Test --log-file argument enables file logging
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 8. Add error handling and edge cases


  - Implement retry logic with exponential backoff for file lock errors
  - Add validation to prevent circular references (destination within source)
  - Add handling for symlinks (skip them to avoid loops)
  - Add handling for hidden files (decide whether to process or skip)
  - Implement path traversal validation for security
  - _Requirements: 6.3_

- [ ]* 8.1 Write unit tests for error scenarios
  - Test retry logic for locked files
  - Test circular reference detection
  - Test symlink handling
  - Test path traversal prevention
  - _Requirements: 6.3_

- [x] 9. Create documentation


  - Write README.md with project overview, installation instructions, and usage examples
  - Add docstrings to all classes and functions with parameter and return value descriptions
  - Create examples/ directory with sample usage scripts
  - Document configuration file format and options
  - _Requirements: 8.4, 8.3_

- [x] 10. Add entry point and packaging


  - Configure setup.py or pyproject.toml with entry point for CLI command
  - Test installation with pip install -e .
  - Verify CLI command works after installation (e.g., file-organizer watch)
  - Create standalone script version for users without pip
  - _Requirements: 8.5_

- [x] 11. Final checkpoint - Ensure all tests pass



  - Run all unit tests and verify they pass
  - Run all property-based tests and verify they pass
  - Check code coverage and ensure critical paths are tested
  - Test on multiple platforms if possible (Windows, macOS, Linux)
  - Verify CLI commands work as expected
  - Test with real files in a test Downloads folder
