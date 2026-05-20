import pytest

from src.sdk.decorators import agent


class TestAgentDecorator:
    @pytest.mark.parametrize(
        "version",
        [
            "0.0.0",
            "1.2.3",
            "10.20.30",
            "1.0.0-alpha",
            "1.0.0-alpha.1",
            "1.0.0+build.7",
            "2.0.0-rc.1+build.7",
        ],
    )
    def test_agent_accepts_semantic_version(self, version):
        @agent(name="worker", version=version)
        class WorkerAgent:
            pass

        assert WorkerAgent.__agent_config__ == {
            "name": "worker",
            "version": version,
            "description": "",
        }

    def test_agent_uses_default_semantic_version(self):
        @agent(name="worker")
        class WorkerAgent:
            pass

        assert WorkerAgent.__agent_config__["version"] == "1.0.0"

    @pytest.mark.parametrize(
        "version",
        [
            "",
            "1",
            "1.2",
            "1.2.3.4",
            "v1.2.3",
            "01.2.3",
            "1.02.3",
            "1.2.x",
            "1.2.3-01",
            "1.2.3-",
            "1.2.3+",
            1,
            None,
        ],
    )
    def test_agent_rejects_malformed_versions(self, version):
        with pytest.raises(ValueError, match="semantic version format"):
            agent(name="worker", version=version)
