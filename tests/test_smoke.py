import importlib


def test_app_imports():
    module = importlib.import_module("src.main_qt")
    assert hasattr(module, "WordHuntApp")
