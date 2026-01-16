from .database import Base
from sqlalchemy import DATETIME, TIMESTAMP, Boolean, Column, Integer, String, text
from sqlalchemy.sql.expression import null, text
class Post(Base):
    __tablename__="post"
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, default = True)
    created_at = Column(DATETIME(timezone = True), nullable = False, server_default = text('now()'))