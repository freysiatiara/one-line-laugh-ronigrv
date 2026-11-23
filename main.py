"""The One-Line Laugh — entry program.

Reads the single joke line stored in entry.txt (next to this file) and
copies it verbatim to the competition output file. Every path is resolved
from this script's own location or from environment variables, never from
the caller's working directory.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.txt")


def destination():
    direct = os.environ.get("ENTRY_OUTPUT")
    if direct:
        return direct
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        folder = os.environ.get(var)
        if folder:
            return os.path.join(folder, "entry.txt")
    return os.path.join("/output", "entry.txt")


def checked(payload):
    # The gate accepts exactly one line of 1-200 characters, not only
    # whitespace.
    text = payload.decode("utf-8").strip()
    if not text or len(text) > 200 or "\n" in text:
        raise ValueError("entry.txt must hold exactly one line of 1-200 characters")
    return payload


def main():
    with open(SOURCE, "rb") as handle:
        payload = checked(handle.read())
    target = destination()
    folder = os.path.dirname(target)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(payload)
    os.chmod(target, 0o644)


if __name__ == "__main__":
    main()
