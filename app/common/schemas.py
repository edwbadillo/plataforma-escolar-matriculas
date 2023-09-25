from datetime import datetime
from typing import Optional


class TimestampsMixinSchema:
    """Mixin para agregar los campos created_at y updated_at para los schemas que lo
    requieran"""

    created_at: datetime
    updated_at: Optional[datetime] = None
