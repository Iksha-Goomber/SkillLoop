import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build_dir = tempfile.TemporaryDirectory()
        executable = "engine.exe" if os.name == "nt" else "engine"
        cls.bin = Path(cls.build_dir.name) / executable
        compiler = os.environ.get("CXX") or shutil.which("g++") or "g++"
        cmd = [
            compiler, "-std=c++17", "-O2",
            str(Path("cpp_engine") / "src" / "main.cpp"),
            "-o", str(cls.bin),
        ]
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"C++ test-engine compilation failed (exit code {result.returncode}).\\n"
                f"Compiler command: {' '.join(cmd)}\\n"
                f"stdout:\\n{result.stdout}\\nstderr:\\n{result.stderr}"
            )

    @classmethod
    def tearDownClass(cls):
        cls.build_dir.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data = Path(self.tmp.name)
        self.call("init")

    def tearDown(self):
        self.tmp.cleanup()

    def call(self, *args):
        result = subprocess.run(
            [str(self.bin), args[0], str(self.data), *args[1:]],
            cwd=ROOT, check=True, capture_output=True, text=True
        )
        return result.stdout

    def test_sample_data(self):
        self.assertEqual(len(self.call("students").strip().splitlines()), 4)

    def test_reciprocal_match(self):
        rows = self.call("matches", "S001").strip().splitlines()
        self.assertTrue(any(row.startswith("S002\tIksha\t") for row in rows))

    def test_one_sided_overlap_is_excluded(self):
        self.call(
            "add_student", "S005", "OneWay", "oneway@example.com", "Design",
            "1", "C++;Rust", "Go", "Weekends", "Online"
        )
        rows = self.call("matches", "S001").strip().splitlines()
        self.assertFalse(any(row.startswith("S005\t") for row in rows))

    def test_exchange_lifecycle(self):
        self.call("create_exchange", "S001", "S002", "Python")
        self.assertIn("Pending", self.call("exchanges"))
        self.call("update_exchange", "EX1001", "Accepted")
        self.assertIn("Accepted", self.call("exchanges"))

    def test_polymorphic_demo(self):
        output = self.call("user_demo")
        self.assertIn("Student\t", output)
        self.assertIn("Admin\t", output)

    def test_profile_update(self):
        self.call(
            "update_student", "S001", "Aman Updated", "aman@example.com",
            "Computer Science", "2", "Java;C++", "Python", "Weekends", "Hybrid"
        )
        self.assertIn("Aman Updated", self.call("students"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
