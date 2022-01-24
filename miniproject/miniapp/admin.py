
from django.contrib import admin
from .models import Cat,CatBoard,CatPhoto,Feed,Location,User,UserHasCat

admin.site.register(Cat)
admin.site.register(CatBoard)
admin.site.register(CatPhoto)
admin.site.register(Feed)
admin.site.register(Location)
admin.site.register(User)
admin.site.register(UserHasCat)
