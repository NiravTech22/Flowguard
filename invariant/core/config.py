import uuid
import hashlib
import time
from typing import Dict, Any

class ExperimentConfig:
    """Tracks experiment configuration and run identifiers for reproducibility."""
    
    def __init__(self, config_data: Dict[str, Any], run_id: str = None, timestamp: float = None):
        self.run_id = run_id or str(uuid.uuid4())
        self.timestamp = timestamp or time.time()
        self.config_data = config_data
        self.config_hash = self._generate_hash(config_data)

    def _generate_hash(self, data: Dict[str, Any]) -> str:
        """Generates a stable hash of the configuration dictionary."""
        # Sort keys for stability
        serialized = str(sorted(data.items())).encode('utf-8')
        return hashlib.sha256(serialized).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "config_hash": self.config_hash,
            "config": self.config_data
        }
