from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime

from objects.schemas.base import Base


class BeatmapSchema(Base):
    __tablename__ = "beatmaps"
    __table_args__ = {"schema": "calculator"}

    id: Mapped[int] = mapped_column(primary_key=True)
    set_id: Mapped[int] = mapped_column(nullable=False)
    md5: Mapped[str] = mapped_column(nullable=False)
    artist: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    version: Mapped[str] = mapped_column(nullable=False)
    creator: Mapped[str] = mapped_column(nullable=False)
    last_update: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
    )
    total_length: Mapped[int] = mapped_column()
    max_combo: Mapped[int] = mapped_column()
    bpm: Mapped[float] = mapped_column()
    status: Mapped[int | None] = mapped_column(nullable=True)
