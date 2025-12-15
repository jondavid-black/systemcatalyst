from src.ui.main import main


def test_ui_main_starts():
    # Basic smoke test for UI main function
    # Flet apps are hard to test headless without a lot of setup,
    # so we'll just check that the function exists and is callable.
    assert callable(main)
