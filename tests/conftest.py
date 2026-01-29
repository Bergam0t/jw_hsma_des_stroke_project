"""
Test configuration - preventing mutation between tests due to global g
"""

import copy
import pytest
from stroke_ward_model.inputs import g


# Capture the original class attribute values once, at import time.
_ORIGINAL_G_STATE = {
    name: getattr(g, name)
    for name in dir(g)
    if not name.startswith("__") and not callable(getattr(g, name))
}


def reset_g_to_original():
    for name, value in _ORIGINAL_G_STATE.items():
        setattr(g, name, copy.deepcopy(value))


@pytest.fixture(autouse=True)
def reset_globals_between_tests():
    reset_g_to_original()
    yield
    reset_g_to_original()
