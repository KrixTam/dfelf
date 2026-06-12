import argparse
import glob
import os
import shutil
import subprocess
import sys


def _remove_path(path: str):
    if not os.path.exists(path):
        return
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def clean(root_dir: str):
    targets = [
        ".coverage",
        ".pytest_cache",
        "build",
        "dist",
        "htmlcov",
        "log",
        "logs",
        "output",
    ]
    for name in targets:
        _remove_path(os.path.join(root_dir, name))
    for pattern in ["*.egg-info", "*.dist-info"]:
        for path in glob.glob(os.path.join(root_dir, pattern)):
            _remove_path(path)


def ensure_build_installed(no_install: bool):
    try:
        import build
        return
    except Exception:
        if no_install:
            raise
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "build"],
        check=True,
    )


def build_package(root_dir: str, sdist: bool, wheel: bool):
    args = [sys.executable, "-m", "build"]
    if sdist and not wheel:
        args.append("--sdist")
    if wheel and not sdist:
        args.append("--wheel")
    subprocess.run(args, cwd=root_dir, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean-only", action="store_true")
    parser.add_argument("--no-clean", action="store_true")
    parser.add_argument("--no-install-build", action="store_true")
    parser.add_argument("--sdist", action="store_true")
    parser.add_argument("--wheel", action="store_true")
    args = parser.parse_args()

    root_dir = os.path.abspath(os.path.dirname(__file__))
    if not args.no_clean:
        clean(root_dir)

    if args.clean_only:
        return

    ensure_build_installed(args.no_install_build)
    sdist = args.sdist or (not args.sdist and not args.wheel)
    wheel = args.wheel or (not args.sdist and not args.wheel)
    build_package(root_dir, sdist=sdist, wheel=wheel)


if __name__ == "__main__":
    main()
