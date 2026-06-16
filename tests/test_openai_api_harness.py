from pathlib import Path

from openai_api_harness import OPENAI_RESPONSES_URL, build_request, run_harness
from openai_api_harness import _load_regression_case as load_regression_case

ROOT = Path(__file__).resolve().parents[1]


def test_openai_harness_builds_responses_api_request() -> None:
    case = load_regression_case(ROOT, "ZC-02")
    request = build_request(ROOT, case, "gpt-5.5")

    assert request["model"] == "gpt-5.5"
    assert request["input"][0]["role"] == "developer"
    assert request["input"][1]["role"] == "user"
    assert request["input"][1]["content"][0]["text"] == case.prompt
    assert "context/因明推理引擎.md" in request["input"][0]["content"][0]["text"]
    assert request["reasoning"]["effort"] == "low"


def test_openai_harness_builds_chat_completions_request() -> None:
    case = load_regression_case(ROOT, "ZC-02")
    request = build_request(ROOT, case, "volcengine-model", api_surface="chat-completions")

    assert request["model"] == "volcengine-model"
    assert request["messages"][0]["role"] == "system"
    assert request["messages"][1]["role"] == "user"
    assert request["messages"][1]["content"] == case.prompt
    assert "context/因明推理引擎.md" in request["messages"][0]["content"]


def test_openai_harness_dry_run_does_not_require_api_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = run_harness(root=ROOT, case_id="ZC-03", model="gpt-5.5", prompt_override=None, live=False)

    assert result.mode == "dry-run"
    assert result.endpoint == OPENAI_RESPONSES_URL
    assert result.base_url == "https://api.openai.com/v1"
    assert result.api_surface == "responses"
    assert result.output_text is None
    assert "context/摄类学工具箱.md" in result.reference_files


def test_openai_compatible_harness_can_target_chat_completions_base_url(monkeypatch) -> None:
    monkeypatch.delenv("VOLCENGINE_OPENAI_API_KEY", raising=False)

    result = run_harness(
        root=ROOT,
        case_id="ZC-02",
        model="volcengine-model",
        prompt_override=None,
        base_url="https://example.volcengine.test/api/v3/",
        api_surface="chat-completions",
        api_key_env="VOLCENGINE_OPENAI_API_KEY",
        live=False,
    )

    assert result.mode == "dry-run"
    assert result.endpoint == "https://example.volcengine.test/api/v3/chat/completions"
    assert result.api_key_env == "VOLCENGINE_OPENAI_API_KEY"
    assert result.request["messages"][0]["role"] == "system"


def test_provider_route_applies_volcengine_defaults(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)
    monkeypatch.delenv("OPENAI_API_SURFACE", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY_ENV", raising=False)

    result = run_harness(
        root=ROOT,
        case_id="ZC-02",
        provider_route="volcengine_openai_compatible",
        model=None,
        prompt_override=None,
        live=False,
    )

    assert result.provider_route == "volcengine_openai_compatible"
    assert result.model == "ark-code-latest"
    assert result.base_url == "https://ark.cn-beijing.volces.com/api/coding/v3"
    assert result.endpoint == "https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions"
    assert result.api_surface == "chat-completions"
    assert result.api_key_env == "VOLCENGINE_OPENAI_API_KEY"


def test_provider_route_rejects_unknown_route() -> None:
    try:
        run_harness(
            root=ROOT,
            case_id="ZC-02",
            provider_route="unknown_provider",
            model=None,
            prompt_override=None,
            live=False,
        )
    except ValueError as exc:
        assert "Unknown provider route: unknown_provider" in str(exc)
    else:
        raise AssertionError("unknown provider route should fail")


def test_openai_harness_live_requires_api_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    try:
        run_harness(root=ROOT, case_id="ZC-02", model="gpt-5.5", prompt_override=None, live=True)
    except RuntimeError as exc:
        assert "OPENAI_API_KEY" in str(exc)
    else:
        raise AssertionError("live OpenAI API harness should require OPENAI_API_KEY")


def test_openai_compatible_harness_live_uses_configured_key_env(monkeypatch) -> None:
    monkeypatch.delenv("VOLCENGINE_OPENAI_API_KEY", raising=False)

    try:
        run_harness(
            root=ROOT,
            case_id="ZC-02",
            model="volcengine-model",
            prompt_override=None,
            base_url="https://example.volcengine.test/api/v3",
            api_surface="chat-completions",
            api_key_env="VOLCENGINE_OPENAI_API_KEY",
            live=True,
        )
    except RuntimeError as exc:
        assert "VOLCENGINE_OPENAI_API_KEY" in str(exc)
    else:
        raise AssertionError("live OpenAI-compatible harness should require the configured API key env var")
