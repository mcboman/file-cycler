# FileRotationManager

The **FileRotationManager** is a Python library designed to manage file rotation in a specified directory. It automatically organizes files into dated folders and applies a retention policy to remove old files, ensuring that you keep only the data you need.

## Key Features:

- **Automated File Rotation**: Automatically moves files into dated folders based on the current date.
  
- **Retention Policy**: Cleans up old files based on a user-defined retention period, specified in days.

- **Customizable Working Directory**: Allows you to set the working directory where the file rotation and retention will occur.

- **Version Listing**: Provides a method to list all available versions (dated folders) in the working directory.

This library is particularly useful for applications that generate time-sensitive data files that need to be retained for a specific period.
