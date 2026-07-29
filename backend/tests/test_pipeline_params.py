"""Per-run pipeline parameters: merge/coerce, defaults endpoint, stored on the job, cmd flag."""
from app.services.pipeline_params import default_parameters, merge_parameters
from app.worker import pipeline_run as pr
from tests.conftest import bearer, user_id
from tests.test_jobs_api import _make_kit, job_payload, no_enqueue  # noqa: F401


def test_default_parameters_has_progressive_threshold():
    d = default_parameters()
    assert isinstance(d.get("progressive_threshold"), bool)
    assert "AlleleAcceptanceThreshold" in d and "negative_name" in d


def test_merge_coerces_and_drops_unknown():
    m = merge_parameters({"AlleleAcceptanceThreshold": "3", "progressive_threshold": "false", "bogus": 1})
    assert m["AlleleAcceptanceThreshold"] == 3 and isinstance(m["AlleleAcceptanceThreshold"], int)
    assert m["progressive_threshold"] is False
    assert "bogus" not in m
    assert m["negative_name"] == default_parameters()["negative_name"]   # untouched default


def test_defaults_endpoint(client, admin_token):
    r = client.get("/api/jobs/parameters/defaults", headers=bearer(admin_token))
    assert r.status_code == 200 and "progressive_threshold" in r.json()


def test_job_stores_merged_parameters(client, catalog, admin_token, no_enqueue):
    kit_id = _make_kit(client, admin_token, assigned_ids=[])
    payload = {**job_payload(kit_id), "parameters": {"AlleleAcceptanceThreshold": 5}}
    r = client.post("/api/jobs", json=payload, headers=bearer(admin_token))
    assert r.status_code == 201, r.text
    params = r.json()["parameters"]
    assert params["AlleleAcceptanceThreshold"] == 5          # override applied
    assert "progressive_threshold" in params                # full merged set stored


def test_build_nextflow_cmd_params_flag():
    cmd = pr.build_nextflow_cmd(
        pipeline_dir="/p", input_tsv="/i.tsv", run_dir="/r", profile="local",
        min_identity=0.9, min_overlap=20, parameters_file_path="/r/inputs/parameters.json")
    assert "--parameters_file_path" in cmd and "/r/inputs/parameters.json" in cmd
    cmd2 = pr.build_nextflow_cmd(
        pipeline_dir="/p", input_tsv="/i.tsv", run_dir="/r", profile="local",
        min_identity=0.9, min_overlap=20)
    assert "--parameters_file_path" not in cmd2
