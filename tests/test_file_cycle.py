import os
import tempfile
import time
import unittest
from datetime import datetime, timedelta

from src.file_cycle import FileCycle


class TestFileCycle(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.workdir_prefix = self.tmp_dir.name
        self.workdir = 'rotation'
        self.retention_days = 30
        self.file_rotation_manager = FileCycle(
            workdir_prefix=self.workdir_prefix,
            workdir=self.workdir,
            retention_days=self.retention_days
        )

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_rotate(self):
        # Create a file in the latest folder
        with open(os.path.join(self.file_rotation_manager.latest_folder, 'test.txt'), 'w') as f:
            f.write('test')

        # Wait for a second to ensure the file has a different timestamp
        time.sleep(1)

        # Rotate the files
        self.file_rotation_manager.rotate()

        # Check that the latest folder is empty
        self.assertEqual(len(os.listdir(self.file_rotation_manager.latest_folder)), 0)

        # Check that the rotated folder exists
        folder_name = datetime.now().strftime("%Y-%m-%d")
        rotated_folder = os.path.join(self.file_rotation_manager.full_workdir, folder_name)
        self.assertTrue(os.path.exists(rotated_folder))

        # Check that the rotated folder contains the rotated file
        rotated_file = os.path.join(rotated_folder, 'test.txt')
        self.assertTrue(os.path.exists(rotated_file))

    def test_apply_retention_policy(self):
        # Create a folder with a date older than the retention period
        old_folder_name = (datetime.now() - timedelta(days=self.retention_days + 31)).strftime("%Y-%m-%d")
        old_folder = os.path.join(self.file_rotation_manager.full_workdir, old_folder_name)
        os.makedirs(old_folder)

        # Create a folder with a date within the retention period
        new_folder_name = (datetime.now() - timedelta(days=self.retention_days - 1)).strftime("%Y-%m-%d")
        new_folder = os.path.join(self.file_rotation_manager.full_workdir, new_folder_name)
        os.makedirs(new_folder)

        # Apply the retention policy
        self.file_rotation_manager._apply_retention_policy()

        # Check that the old folder has been deleted
        self.assertFalse(os.path.exists(old_folder))

        # Check that the new folder still exists
        self.assertTrue(os.path.exists(new_folder))

    def test_list_versions(self):
        # Create some folders
        folder1 = os.path.join(self.file_rotation_manager.full_workdir, '2022-01-01')
        os.makedirs(folder1)
        folder2 = os.path.join(self.file_rotation_manager.full_workdir, '2022-01-02')
        os.makedirs(folder2)

        # List the versions
        versions = self.file_rotation_manager.list_versions()

        # Check that the versions are correct
        self.assertEqual(len(versions), 3)
        self.assertIn('latest', versions)
        self.assertIn('2022-01-01', versions)
        self.assertIn('2022-01-02', versions)
        self.assertIn('2022-01-02', versions)


