import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = PROJECT_ROOT / "repo-security-checker" / "check_repo_security.py"

spec = importlib.util.spec_from_file_location("check_repo_security", CHECKER_PATH)
checker = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["check_repo_security"] = checker
spec.loader.exec_module(checker)


class RepoSecurityCheckerTest(unittest.TestCase):
    def test_normalize_github_url_accepts_browser_url(self):
        url = checker.normalize_github_url("https://github.com/example/demo/tree/main")

        self.assertEqual(url, "https://github.com/example/demo.git")

    def test_scan_target_clones_github_url_before_scanning(self):
        original_clone = checker.clone_repository

        def fake_clone(url, destination_root):
            clone_path = destination_root / "repo"
            clone_path.mkdir()
            (clone_path / "README.md").write_text("# Demo\n", encoding="utf-8")
            (clone_path / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (clone_path / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
            (clone_path / ".gitignore").write_text(".env\n", encoding="utf-8")
            return clone_path

        checker.clone_repository = fake_clone
        try:
            report = checker.scan_target("https://github.com/example/demo")
        finally:
            checker.clone_repository = original_clone

        self.assertEqual(report.source, "https://github.com/example/demo.git")
        self.assertEqual(report.score, 100)

    def test_clean_minimal_repo_has_no_basic_file_findings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
            (root / ".gitignore").write_text(".env\n", encoding="utf-8")

            report = checker.run_checks(root)

        self.assertEqual(report.score, 100)
        self.assertEqual(report.findings, [])

    def test_missing_security_policy_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / ".gitignore").write_text(".env\n", encoding="utf-8")

            report = checker.run_checks(root)

        check_ids = {finding.check_id for finding in report.findings}
        self.assertIn("missing-security-policy", check_ids)

    def test_sensitive_env_file_is_high_severity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
            (root / ".gitignore").write_text(".env\n", encoding="utf-8")
            (root / ".env").write_text("TOKEN=example-only\n", encoding="utf-8")

            report = checker.run_checks(root)

        sensitive = [finding for finding in report.findings if finding.check_id == "sensitive-file"]
        self.assertEqual(len(sensitive), 1)
        self.assertEqual(sensitive[0].severity, "high")

    def test_hardcoded_secret_assignment_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
            (root / ".gitignore").write_text(".env\n", encoding="utf-8")
            variable_name = "API" + "_KEY"
            fake_value = "abcdefghijklmnopqrstuvwxyz"
            (root / "settings.py").write_text(f"{variable_name} = '{fake_value}'\n", encoding="utf-8")

            report = checker.run_checks(root)

        check_ids = {finding.check_id for finding in report.findings}
        self.assertIn("assigned-secret", check_ids)


if __name__ == "__main__":
    unittest.main()
