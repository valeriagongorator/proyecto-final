import src.main_qt as main_qt


def _make_app():
    return main_qt.WordHuntApp.__new__(main_qt.WordHuntApp)


def test_valid_straight_word_is_accepted():
    app = _make_app()
    app.current_board = [
        ["A", "X", "X"],
        ["X", "B", "X"],
        ["X", "X", "C"],
    ]
    app.selected_positions = [(0, 0), (1, 1), (2, 2)]
    app.hidden_words = ["ABC"]
    app.found_words = []

    assert app._find_selected_word() == "ABC"


def test_non_straight_path_is_rejected():
    app = _make_app()
    app.current_board = [
        ["A", "B", "X"],
        ["X", "C", "X"],
        ["X", "X", "X"],
    ]
    app.selected_positions = [(0, 0), (0, 1), (1, 1)]
    app.hidden_words = ["ABC"]
    app.found_words = []

    assert app._find_selected_word() is None


def test_confirm_selection_penalizes_wrong_word(monkeypatch):
    app = _make_app()
    app.current_board = [
        ["A", "B", "C"],
        ["X", "X", "X"],
        ["X", "X", "X"],
    ]
    app.selected_positions = [(0, 0), (0, 1), (0, 2)]
    app.selected_letters = ["A", "B", "C"]
    app.hidden_words = ["DEF"]
    app.found_words = []
    app.lives = 3

    class FakeLabel:
        def setText(self, _text):
            pass

    app.word_preview = FakeLabel()

    called = {"wrong": False}

    def fake_wrong():
        called["wrong"] = True

    monkeypatch.setattr(app, "_rebuild_board_visuals", lambda: None)
    monkeypatch.setattr(app, "_wrong_word", fake_wrong)

    app.confirm_selection()

    assert called["wrong"] is True
