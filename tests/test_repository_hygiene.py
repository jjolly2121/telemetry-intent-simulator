import subprocess
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class RepositoryHygieneTests(unittest.TestCase):
    def test_readme_does_not_contain_local_machine_paths(self):
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertNotIn("/Users/", readme)
        self.assertNotIn("C:\\Users\\", readme)

    def test_generated_files_are_not_tracked(self):
        tracked_files = subprocess.check_output(
            ["git", "ls-files"],
            cwd=REPOSITORY_ROOT,
            text=True,
        ).splitlines()

        generated_files = [
            path
            for path in tracked_files
            if path == ".DS_Store"
            or path == "="
            or "__pycache__" in Path(path).parts
            or path.endswith(".pyc")
        ]

        self.assertEqual(generated_files, [])


if __name__ == "__main__":
    unittest.main()
