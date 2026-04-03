"""Export the OpenAPI schema from the FastAPI app to a JSON file."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app

output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/openapi.json")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(app.openapi(), indent=2))
print(f"OpenAPI schema written to {output}")
