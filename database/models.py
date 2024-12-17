from sqlalchemy import Column, Integer, String, Float, ARRAY, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ProductName(Base):
    __tablename__ = "product_names"
    
    id = Column(Integer, primary_key=True, index=True)
    original_description = Column(String)
    generated_name = Column(String)
    keywords = Column(ARRAY(String))
    score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class Keyword(Base):
    __tablename__ = "keywords"
    
    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, unique=True, nullable=False)
    search_volume = Column(Integer)  # 搜索量
    competition_score = Column(Float)  # 竞争度分数
    relevance_score = Column(Float)  # 相关性分数
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 创建索引以加快查询
    __table_args__ = (
        Index('idx_keyword_search', keyword, search_volume.desc()),
    ) 