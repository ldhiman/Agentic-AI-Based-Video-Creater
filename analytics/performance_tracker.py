import json
from datetime import datetime
from pathlib import Path


LOG_FILE = "analytics_log.json"


def log_video(data):
    if Path(LOG_FILE).exists():
        logs = json.loads(Path(LOG_FILE).read_text())
    else:
        logs = []

    data["timestamp"] = datetime.utcnow().isoformat()
    logs.append(data)

    Path(LOG_FILE).write_text(json.dumps(logs, indent=2))