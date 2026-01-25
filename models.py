from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from datetime import datetime
from typing import List

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)

    ads: Mapped[List["Ad"]] = relationship(back_populates="owner", lazy="selectin")

    def __repr__(self):
        return f"User(id={self.id}, email='{self.email}')"

    def to_dict(self):
        return {'id': self.id, 'email': self.email}

class Ad(Base):
    __tablename__ = 'ad'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

    owner: Mapped["User"] = relationship(back_populates="ads", lazy="selectin")

    def __repr__(self):
        return f"Ad(id={self.id}, title='{self.title}', owner_id={self.owner_id})"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'owner_id': self.owner_id
        }
