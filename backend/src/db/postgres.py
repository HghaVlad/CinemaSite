from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings


Base = declarative_base()

engine = create_async_engine(settings.database_url, echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, autocommit=False, autoflush=False)


async def get_postgres_session() -> AsyncSession:

    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()