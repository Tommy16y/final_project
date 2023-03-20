from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    

    def has_permission(self, request, view): #GET,POST
        # print(request.method)
        # print(request.user.is_authenticated)
        # print(SAFE_METHODS)

        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj): #Get by id,PUT,PATCH,DELETE
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user == obj.owner