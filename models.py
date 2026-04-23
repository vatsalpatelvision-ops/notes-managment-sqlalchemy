from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime



class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    note_tags = relationship("NoteTag", back_populates="note")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    note_tags = relationship("NoteTag", back_populates="tag")


class NoteTag(Base):
    __tablename__ = "note_tags"

    id = Column(Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)

    note = relationship("Note", back_populates="note_tags")
    tag = relationship("Tag", back_populates="note_tags")