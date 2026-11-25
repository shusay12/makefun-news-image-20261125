#!/usr/bin/env python3
"""news-image-20261125 entrypoint.

Copies the front-page image (entry.png, rendered by build_image.py in
this session) to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
No network, no randomness: two runs write the same bytes.
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
