from datetime import datetime, timezone
from sqlalchemy import create_engine, DateTime, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from app.settings import get_settings

class Base(DeclarativeBase): pass
class MarketBar(Base):
    __tablename__ = "prices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    open: Mapped[float] = mapped_column(Float); high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float); close: Mapped[float] = mapped_column(Float)
    volume: Mapped[float] = mapped_column(Float, default=0)
    __table_args__ = (UniqueConstraint("symbol", "timestamp"),)
class FeatureSnapshot(Base):
    __tablename__ = "features"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    name: Mapped[str] = mapped_column(String(64)); value: Mapped[float] = mapped_column(Float)
class DataSource(Base):
    __tablename__ = "data_sources"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String(64)); retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)); details: Mapped[str] = mapped_column(Text, default="")

def get_engine():
    return create_engine(get_settings().database_url, future=True)
def init_db() -> None:
    get_settings().ensure_data_directory(); Base.metadata.create_all(get_engine())
def session_factory():
    return sessionmaker(bind=get_engine(), expire_on_commit=False)
