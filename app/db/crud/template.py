from typing import List
from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import TemplateModel
from models.form.config import TemplateForm


async def insert_template(db: AsyncSession, robot_id: int, name: str, content: str):
    db.add(TemplateModel(robot_id=robot_id, name=name, content=content))


async def update_template(db: AsyncSession, robot_id: int, template_form: TemplateForm):
    stmt = select(TemplateModel).filter(TemplateModel.robot_id == robot_id).filter(
        TemplateModel.name == template_form.name)
    model = await db.scalar(stmt)
    if model is None:
        return
    model.content = template_form.content
    model.parse_mode = template_form.parse_mode


async def delete_template(db: AsyncSession, ids: List[int]):
    stmt = delete(TemplateModel).where(TemplateModel.id.in_(ids))
    await db.execute(stmt)


async def delete_template_by_robot_id(db: AsyncSession, robot_ids: List[int]):
    stmt = delete(TemplateModel).where(TemplateModel.robot_id.in_(robot_ids))
    await db.execute(stmt)


async def get_template_model(db: AsyncSession, robot_id: int, name: str) -> TemplateModel:
    stmt = select(TemplateModel).filter(TemplateModel.robot_id == robot_id).filter(TemplateModel.name == name)
    model = await db.scalar(stmt)
    return model


async def get_template_model_all(db: AsyncSession, robot_id: int) -> List[TemplateModel]:
    stmt = select(TemplateModel).filter(TemplateModel.robot_id == robot_id)
    models = await db.scalars(stmt)
    return models.all()


async def get_template_content(db: AsyncSession, robot_id: int, name: str) -> [str, str]:
    stmt = select(TemplateModel).where(and_(TemplateModel.robot_id == robot_id, TemplateModel.name == name))
    model = await db.scalar(stmt)
    if model:
        return model.content, model.get_parse_mode()
    else:
        return '', None

