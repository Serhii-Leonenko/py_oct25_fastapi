from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    first_name: Mapped[str] = mapped_column(
        String(65),
        nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(65),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )

    projects: Mapped[list["Project"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    tasks: Mapped[list["Task"]] = relationship(
        secondary="task_assignees", back_populates="assignees"
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"