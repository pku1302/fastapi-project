from app.schemas.comment_schema import CommentRead, CommentReadWithChildren
from typing import List

def build_comment_tree(comments: List[CommentRead]):
    comment_map = {}
    roots = []

    for c in comments:
        node = CommentReadWithChildren.model_validate(c)
        node.children = []
        if c.is_deleted:
            node.content = "삭제된 댓글입니다"
        comment_map[c.id] = node
        

    for c in comments:
        node = comment_map[c.id]

        if c.parent_id is None:
            roots.append(node)
        else:
            parent = comment_map.get(c.parent_id)
            if parent:
                parent.children.append(node)
    
    return roots