from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileBucketUrl:
    url: str
    expires_at: datetime
