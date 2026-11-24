"""Fortune Cookie Wisdom for Developers — entry generator.

Writes one original fortune-cookie line for a software developer to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output). Pure standard library.
"""

import os

ENTRY = "Your code will compile on the first try today. Do not ask why. Do not touch anything. Walk away slowly."

MAX_CHARS = 120


def validate(text: str) -> None:
    """Enforce the competition gate: 1-120 chars, single line, not blank."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text:
        raise ValueError("entry must not be empty")
    if not text.strip():
        raise ValueError("entry must not be blank")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, max is {MAX_CHARS}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    # UTF-8 round trip must be exact; reject characters that cannot be
    # written back byte-identically (e.g. lone surrogates).
    if text.encode("utf-8").decode("utf-8") != text:
        raise ValueError("entry is not clean UTF-8")


def verify_output(path: str, expected: bytes) -> int:
    """Read the file back and confirm it is exactly the expected bytes.

    Returns the byte count. Raises on any mismatch, missing file, or
    a trailing newline (the entry must end on its last character).
    """
    with open(path, "rb") as f:
        landed = f.read()
    if landed != expected:
        raise RuntimeError(
            f"entry.txt mismatch: on disk {len(landed)} bytes, "
            f"expected {len(expected)} bytes"
        )
    if landed.endswith(b"\n") or landed.endswith(b"\r"):
        raise RuntimeError("entry.txt must not end with a newline")
    validate(landed.decode("utf-8"))
    return len(landed)


def output_path() -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def main() -> None:
    validate(ENTRY)
    path = output_path()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read back and re-validate byte for byte what landed on disk.
    size = verify_output(path, data)
    print(f"Wrote {size} bytes to {path}")


if __name__ == "__main__":
    main()
