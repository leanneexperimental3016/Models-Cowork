import importlib.util
import json
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).parents[1] / "model-cowork" / "model_cowork.py"
SPEC = importlib.util.spec_from_file_location("model_cowork", MODULE_PATH)
MC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MC)


class RouterTests(unittest.TestCase):
    def test_all_declared_scenarios_route(self):
        for task_type in MC.TASK_CAPABILITIES:
            self.assertTrue(MC.route(task_type, set(), None, "balanced"), task_type)

    def test_unavailable_models_are_excluded(self):
        result = MC.route("mechanical", {"qwen3:4b"}, "ollama", "balanced")
        self.assertEqual([item["model"] for item in result], ["qwen3:4b"])

    def test_ollama_latest_alias_matches_seed(self):
        result = MC.route("backend-api", {"qwen2.5-coder:latest"}, "ollama", "balanced")
        self.assertEqual([item["model"] for item in result], ["qwen2.5-coder"])

    def test_local_private_never_routes_cloud(self):
        result = MC.route("backend-api", set(), None, "local-private")
        registry = {item["id"]: item for item in MC.load_registry()}
        self.assertTrue(result)
        self.assertTrue(all(registry[item["model"]]["privacy"] == "local" for item in result))

    def test_file_conflict_is_rejected(self):
        ledger = {"assignments": [
            {"id": "a", "status": "active", "files": ["src/App.tsx"]},
            {"id": "b", "status": "planned", "files": ["src\\app.tsx"]},
        ]}
        with self.assertRaisesRegex(ValueError, "ownership conflict"):
            MC.assert_no_file_conflicts(ledger)

    def test_completed_assignment_releases_file(self):
        ledger = {"assignments": [
            {"id": "a", "status": "integrated", "files": ["src/App.tsx"]},
            {"id": "b", "status": "active", "files": ["src/App.tsx"]},
        ]}
        MC.assert_no_file_conflicts(ledger)

    def test_registry_is_valid_json_and_unique(self):
        models = MC.load_registry()
        ids = [item["id"] for item in models]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(item["hosts"] and item["capabilities"] for item in models))


if __name__ == "__main__":
    unittest.main()
