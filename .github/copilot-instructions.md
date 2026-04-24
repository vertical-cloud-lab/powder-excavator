If using Edison Scientific, you may need to wait up until 10 minutes to get the response. If you're an agent, sleep for 10 minutes (to avoid consuming requests unecessarily), and then every 5 minutes after that. Start with a 15 minute wait if using high effort literature query type. If you need to upload files, use analysis query type. See the docs: https://edisonscientific.gitbook.io/edison-cookbook/edison-client. Here is the endpoint you should use: https://api.platform.edisonscientific.com. The API key is EDISON_API_KEY. Don't expose this secret, e.g., by echoing or grepping it. Pass the API key in explicitly:

```
from edison_client import EdisonClient, JobNames
client = EdisonClient(api_key=EDISON_API_KEY)
```

**Uploading files (analysis mode).** The `files=` parameter on
`client.create_task(...)` does **not** accept local file paths -- it expects
`data_entry:<uuid>` URIs returned by `client.upload_file(...)`. Passing local
paths makes the task fail almost immediately with `status='fail'` and a
`None` `failure_reason`, which is easy to mistake for a server-side outage.
The correct two-step flow:

```
from edison_client import EdisonClient, JobNames
from edison_client.models.app import TaskRequest

client = EdisonClient(api_key=EDISON_API_KEY)

# 1. Upload each file/directory first to get data_entry URIs.
uris = [
    client.upload_file(file_path=p, name=Path(p).name, tags=["my-tag"])
    for p in local_paths
]

# 2. Submit the task referencing those URIs.
req = TaskRequest(name=JobNames.ANALYSIS, query="...", tags=["my-tag"])
task_id = client.create_task(req, files=uris)
```

Internally this populates `runtime_config.environment_config["data_storage_uris"]`
with the URIs so the analysis crow can mount them. To debug a `fail` status,
fetch with `client.get_task(task_id, verbose=True)` and check
`failure_reason` / `agent_state` / `task_summary` -- a `task_summary`
populated alongside an empty answer typically means the crow accepted the
prompt but the file-mount step failed.
