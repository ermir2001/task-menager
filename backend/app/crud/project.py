from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def create_project(db: Session, project: ProjectCreate, author_id: int):
    db_project = Project(
       author_id = author_id,
       name = project.name,
       description = project.description
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, db_project: Project, project_data: ProjectUpdate):
    if project_data.name is not None:
        db_project.name = project_data.name
    if project_data.description is not None:
        db_project.description = project_data.description
    
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db: Session, author_id: int):
    return db.query(Project).filter(Project.author_id == author_id).all()

def get_project(db: Session, project_id: int, author_id: int):
    return db.query(Project).filter(
            Project.id == project_id,
            Project.author_id == author_id,

        ).first()

def delete_project(db: Session, db_project: Project):
    db.delete(db_project)
    db.commit()
    return db_project