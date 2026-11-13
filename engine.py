"""Python adapter for the C++17 SkillLoop engine. Business rules live in C++."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CPP = ROOT / "cpp_engine"
BUILD = ROOT / ".build"
BINARY = BUILD / ("skillloop_engine.exe" if os.name == "nt" else "skillloop_engine")

class EngineError(RuntimeError):
    pass


def _compiler() -> str:
    """Return an explicit compiler path so Python and the terminal use the same executable."""
    configured = os.environ.get("CXX", "").strip()
    if configured:
        candidate = shutil.which(configured) or configured
        if Path(candidate).exists() or shutil.which(candidate):
            return candidate
        raise EngineError(f"The CXX compiler setting points to a missing file: {configured}")
    found = shutil.which("g++")
    if not found:
        raise EngineError(
            "A C++17 compiler (g++) was not found on PATH. "
            "Install MinGW-w64/MSYS2 GCC and reopen the terminal."
        )
    return found


def ensure_engine() -> Path:
    BUILD.mkdir(parents=True, exist_ok=True)
    sources = [
        CPP / "src" / "main.cpp",
    ]
    newest_source = max(path.stat().st_mtime for path in sources)
    if BINARY.exists() and BINARY.stat().st_mtime >= newest_source:
        return BINARY

    compiler = _compiler()
    # Relative source paths and a project-local build directory avoid Windows
    # drive/path conversion problems in MSYS2/MinGW subprocesses.
    cmd = [
        compiler, "-std=c++17", "-O2",
        str(Path("cpp_engine") / "src" / "main.cpp"),
        "-o", str(BINARY),
    ]
    try:
        result = subprocess.run(
            cmd, cwd=ROOT, capture_output=True, text=True, timeout=120
        )
    except FileNotFoundError as exc:
        raise EngineError(
            f"Could not start the C++ compiler: {compiler}. "
            "Check that g++ is installed and available on PATH."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise EngineError("C++ engine compilation timed out after 120 seconds.") from exc

    if result.returncode != 0:
        details = (result.stderr or result.stdout or "Compiler returned no diagnostic text.").strip()
        raise EngineError(
            f"C++ engine compilation failed (exit code {result.returncode}).\n"
            f"Compiler: {compiler}\nCommand: {' '.join(cmd)}\n{details[-8000:]}"
        )
    if not BINARY.exists():
        raise EngineError(
            f"The compiler reported success but did not create the executable: {BINARY}"
        )
    return BINARY


def run(command: str, *args: str) -> list[list[str]]:
    exe = ensure_engine()
    DATA.mkdir(exist_ok=True)
    proc = subprocess.run(
        [str(exe), command, str(DATA), *map(str, args)],
        cwd=ROOT, capture_output=True, text=True, timeout=30
    )
    if proc.returncode:
        raise EngineError(proc.stderr.strip() or "C++ engine returned an error")
    return [line.split("\t") for line in proc.stdout.splitlines() if line.strip()]


def initialise(): return run("init")
def students(): return run("students")
def add_student(student_id, name, email, course, year, teaches, learns, availability, mode):
    return run("add_student", student_id, name, email, course, year, ";".join(teaches), ";".join(learns), availability, mode)
def update_student(student_id, name, email, course, year, teaches, learns, availability, mode):
    return run("update_student", student_id, name, email, course, year, ";".join(teaches), ";".join(learns), availability, mode)
def matches(student_id): return run("matches", student_id)
def exchanges(): return run("exchanges")
def create_exchange(requester, target, skill): return run("create_exchange", requester, target, skill)
def update_exchange(exchange_id, status): return run("update_exchange", exchange_id, status)
def user_demo(): return run("user_demo")
