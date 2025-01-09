# weather/urls.py
from django.urls import path
from .views import (
    register,
    user_login,
    user_logout,
    weather_view,
    post_list,
    post_create,
    post_update,
    post_delete,
    home,
)

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('weather/', weather_view, name='weather'),
    path('posts/', post_list, name='post_list'),
    path('posts/create/', post_create, name='post_create'),
    path('posts/update/<int:post_id>/', post_update, name='post_update'),
    path('posts/delete/<int:post_id>/', post_delete, name='post_delete'),
]

# Summary of Steps to Resolve the ImportError

# 1. **Verify the `City` Model**: Ensure that the `City` model is defined in your `models.py` file. If it’s missing, add it as shown in the example.

# 2. **Check for Typos**: Confirm that the import statement in `views.py` matches the model name exactly.

# 3. **Run Migrations**: If you’ve recently added or modified the `City` model, run the migration commands to apply changes to the database.

# 4. **Avoid Circular Imports**: Review your import structure to prevent circular dependencies that could lead to import errors.

# 5. **Restart the Server**: After making changes, restart your Django development server to apply the updates.

# 6. **Look for Additional Errors**: If the problem persists, check the console for any other error messages that might provide further insight.

# ### Example of Complete Setup

# Here’s how your files should look:

# **`models.py`**:

# ```python
# weather/models.py
# from django.db import models

# class City(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self name

# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self title
# ````

