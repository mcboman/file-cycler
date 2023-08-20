# FileCycle: Python File Rotation Manager

**FileCycle** is a Python library designed to manage file rotation in a specified directory. It automatically organizes files into dated folders and applies a retention policy to remove old files. This ensures that you keep only the data you need for a specified period.

## Key Features:

- **Automated File Rotation**: Automatically moves files into dated folders based on the current date.
  
- **Retention Policy**: Cleans up old files based on a user-defined retention period, specified in days.

- **Customizable Working Directory**: Allows you to set the working directory where the file rotation and retention will occur.

- **Version Listing**: Provides a method to list all available versions (dated folders) in the working directory.

This library is particularly useful for applications that generate time-sensitive data files that need to be retained for a specific period.


## Installation

Copy the `FileCycle` class into your project.

## Features

- **Automated File Rotation**: Moves files into dated folders based on the current date.
- **Retention Policy**: Removes old files based on a user-defined retention period.
- **Customizable Working Directory**: Allows you to set the working directory for file rotation.
- **Version Listing**: Lists all available versions (dated folders) in the working directory.

## Usage

### Initialization

Initialize the `FileCycle` class by specifying the working directory prefix, the working directory, and the retention days.

```python
from FileCycle import FileCycle  # Assuming FileCycle is in a file named FileCycle.py

# Initialize with default settings
file_cycle = FileCycle()

# Or specify custom settings
file_cycle = FileCycle(workdir_prefix="/your/prefix", workdir="/your/dir", retention_days=15)