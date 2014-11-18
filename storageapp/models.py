# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from storageapp.database import Base

class ClipMetadata(Base):
    __tablename__ = 'clip_metadata'
    id = Column(Integer, primary_key=True)
    stream_id = Column(Integer, nullable=False)
    start_time = Column(Float, nullable=False)
    stop_time = Column(Float, nullable=False)
    container_format = Column(String(32), nullable=False)
    create_time = Column(DateTime, nullable=False)

    def __init__(self, stream_id, start_time, stop_time, container_format):
        self.stream_id = stream_id
        self.start_time = start_time
        self.stop_time = stop_time
        self.container_format = container_format
        self.create_time = datetime.now()

    def __repr__(self):
        return '<ClipMetadata %r>' % (self.id)

    def to_json(self):
        return {
            "clip_id": self.id,
            "start": self.start_time,
            "stop": self.stop_time,
            "stream_id": self.stream_id
        }
