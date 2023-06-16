from .models import Comment


def get_comments_data(comments):
    comments_data = []
    for comment in comments:
        comment_dict = {
            'id': comment.id,
            'scan__id': comment.scan.id,
            'parent_comment': comment.parent_comment_id,
            'isPrimaryComment': comment.isPrimaryComment,
            'user__email': comment.user.email,
            'comment': comment.comment,
            'created_at': comment.created_at,
            'replies': []
        }
        replies = Comment.objects.filter(
            parent_comment_id=comment.id)  # Get replies for the comment
        if replies:
            comment_dict['replies'] = get_comments_data(replies)
        comments_data.append(comment_dict)
    return comments_data