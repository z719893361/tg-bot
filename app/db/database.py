import asyncio
import contextlib
import os
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('MYSQL_URL')

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    async with async_session() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            raise e
        else:
            await db.commit()
        finally:
            await db.close()


@contextlib.asynccontextmanager
async def get_async_db() -> AsyncSession:
    async with async_session() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            raise e
        else:
            await db.commit()
        finally:
            await db.close()


