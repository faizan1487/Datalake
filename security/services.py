# from .models import Comment

# def get_comments_data(comments):
#     comment_ids = [comment.id for comment in comments]
#     comments_data = []
#     comment_mapping = {}

#     # Fetch all the related data in a single query using eager loading
#     comments = Comment.objects.select_related('scan', 'user').filter(id__in=comment_ids)

#     for comment in comments:
#         if comment.parent_comment_id is None:
#             comment_dict = {
#                 'id': comment.id,
#                 'scan__id': comment.scan.id,
#                 'parent_comment': comment.parent_comment_id,
#                 'isPrimaryComment': comment.isPrimaryComment,
#                 'user__email': comment.user.email,
#                 'comment': comment.comment,
#                 'created_at': comment.created_at,
#                 'replies': [],
#             }
#             comments_data.append(comment_dict)
#             comment_mapping[comment.id] = comment_dict

#     for comment in comments:
#         if comment.parent_comment_id is not None:
#             reply_dict = {
#                 'id': comment.id,
#                 'scan__id': comment.scan.id,
#                 'parent_comment': comment.parent_comment_id,
#                 'isPrimaryComment': comment.isPrimaryComment,
#                 'user__email': comment.user.email,
#                 'comment': comment.comment,
#                 'created_at': comment.created_at,
#                 'replies': [],
#             }
#             parent_comment = comment_mapping.get(comment.parent_comment_id)
#             if parent_comment is not None:
#                 parent_comment['replies'].append(reply_dict)

#     return comments_data
