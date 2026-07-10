from sqlalchemy.orm import Mapped, mapped_column

from objects.schemas.base import Base


class ScoreSchema(Base):
    __tablename__ = "scores"
    __table_args__ = {"schema": "calculator"}

    id: Mapped[int] = mapped_column(primary_key=True)
    beatmap_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    md5: Mapped[str] = mapped_column(nullable=False)
    pp: Mapped[float] = mapped_column()
    score: Mapped[int] = mapped_column()
    max_combo: Mapped[int] = mapped_column()
    mods: Mapped[str] = mapped_column()
    acc: Mapped[float] = mapped_column()
    h300: Mapped[int] = mapped_column()
    h100: Mapped[int] = mapped_column()
    h50: Mapped[int] = mapped_column()
    hmiss: Mapped[int] = mapped_column()
    hgeki: Mapped[int] = mapped_column()
    hkatsu: Mapped[int] = mapped_column()
    slidertickhits: Mapped[int] = mapped_column()
    sliderendhits: Mapped[int] = mapped_column()
    grade: Mapped[str] = mapped_column()
    fc: Mapped[bool] = mapped_column()
    date: Mapped[int] = mapped_column()
