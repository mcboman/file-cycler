import shutil
from datetime import datetime, timedelta
from os import getenv, listdir, makedirs, path
from tempfile import gettempdir


class FileCycle():
    """
    Manages file rotation based on specified retention policies.

    Attributes:
        workdir_prefix (str): The prefix for the working directory.
        workdir (str): The name of the working directory.
        full_workdir (str): The full path to the working directory.
        retention_days (int): The number of days to retain old files.
        latest_folder (str): The path to the 'latest' folder within the working directory.
    """
    def __init__(self,
                 workdir_prefix=getenv('WORKDIR_PREFIX', gettempdir()),
                 workdir=getenv('WORKDIR', '/rotation'),
                 retention_days=30):
        """
        Initialize the file rotation manager.

        Parameters:
            workdir_prefix (str): The prefix for the working directory. Defaults to '/tmp'.
            workdir (str): The name of the working directory. Defaults to '/rotation'.
            retention_days (int): The number of days to retain old files. Defaults to 30.
        """
        self.workdir_prefix = workdir_prefix
        self.workdir = workdir
        self.full_workdir = path.join(self.workdir_prefix, self.workdir)
        self.retention_days = retention_days
        self.latest_folder = path.join(
            self.full_workdir,
            "latest")

        if not path.exists(self.full_workdir):
            makedirs(self.latest_folder)

    def rotate(self):
        """
        Rotate the files in the working directory daily.
        Also applies the retention policy to remove old files.
        """
        folder_name = self._get_folder_name()
        dest_folder = path.join(self.full_workdir, folder_name)

        if path.exists(dest_folder):
            shutil.rmtree(dest_folder)

        shutil.move(self.latest_folder, dest_folder)
        makedirs(self.latest_folder)
        self._apply_retention_policy()

    def _get_folder_name(self):
        """
        Generate the folder name based on the current date.

        Returns:
            str: The generated folder name.
        """
        return datetime.now().strftime("%Y-%m-%d")

    def _apply_retention_policy(self):
        """
        Apply the retention policy to remove files older than the specified number of days.
        """
        if self.retention_days is not None:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)

            for folder in listdir(self.full_workdir):
                if folder == "latest":
                    continue

                try:
                    folder_date = datetime.strptime(folder, "%Y-%m-%d")
              
                    if folder_date < cutoff_date:
                        shutil.rmtree(path.join(self.full_workdir, folder))
                except ValueError:
                    continue

    def list_versions(self) -> list[str]:
        """
        List all versions of the rotated files in the working directory.

        Returns:
            list[str]: A list of folder names representing different versions.
        """
        return list(listdir(self.full_workdir))
