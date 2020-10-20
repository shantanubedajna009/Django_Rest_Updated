from rest_framework import permissions

# class BlocklistPermission(permissions.BasePermission):
#     """
#     Global permission check for blocked IPs.
#     """

#     def has_permission(self, request, view):
#         ip_addr = request.META['REMOTE_ADDR']
#         blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
#         return not blocked


class IsUserAuthenticated(permissions.BasePermission):
    
    message = 'You are already authenticated. Please log out to try again.'


    # this function stops normal execution when it returns False
    # in this case if user is authenticated then it returns false
    # whicch stops the execution process
    # if user is not autheenticated then it allows normal execution path
    def has_permission(self, request, view):
        return not request.user.is_authenticated # Invoke this when user is not authenticated
        # invoking this means stop the normal execution and return that defied message insted



class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    message = 'You don\'t have permission to edit this.'

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user