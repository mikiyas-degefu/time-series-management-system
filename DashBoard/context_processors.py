def user_context(request):
    return {
        'logged_in_user': request.user
    }