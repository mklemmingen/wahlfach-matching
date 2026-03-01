"""Allow running as ``python -m wahlfach_matching``."""

import sys

from .cli import main

sys.exit(main())
