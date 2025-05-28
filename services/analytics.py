def get_user_stats(user):
    return {
        'total_boutiques': user.owned_boutiques.count(),
        'total_reviews': user.reviews.count(),
        'total_posts': user.posts.count(),
        'favorite_boutiques': user.favorites.count()
    } 