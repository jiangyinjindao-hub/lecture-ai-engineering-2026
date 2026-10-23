"""質問スクリプトのテスト（LLMもAPIキーも使わない）。"""

from types import SimpleNamespace

import app.ask as ask_module


def test_ask_prints_response_time(monkeypatch, capsys):
    timestamps = iter([10.0, 11.234])
    monkeypatch.setattr(ask_module.time, "perf_counter", lambda: next(timestamps))
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    class FakeClient:
        def __init__(self, *, api_key):
            assert api_key == "test-key"
            self.models = self

        def generate_content(self, *, model, contents):
            assert contents == "question"
            return SimpleNamespace(text="answer", usage_metadata=None)

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)

    assert ask_module.ask("question") == "answer"
    assert "応答時間: 1.234秒" in capsys.readouterr().out
