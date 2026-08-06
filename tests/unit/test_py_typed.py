from pathlib import Path

import together


def test_py_typed_marker_ships_with_package() -> None:
    """PEP 561 requires the marker to sit inside the installed package.

    Checking it relative to the imported module (rather than the repo tree)
    means this also fails if the marker is ever dropped from the built
    distribution.
    """
    package_root = Path(together.__file__).parent
    assert (package_root / "py.typed").is_file()
