from pydantic import BaseModel
from typing import List, Optional

class VideoSignal(BaseModel):
    video_id: str
    title: str
    url: str
    view_count: int
    like_count: int
    comment_count: int

class CommentSignal(BaseModel):
    comment_id: str
    text: str
    like_count: int
    reply_count: int
    author: Optional[str]
    created_at: Optional[str]
