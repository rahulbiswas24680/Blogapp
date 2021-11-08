from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="blog-home"),
    path("category/<category>/", views.CatListView.as_view(), name="category"),
    path("about/", views.about, name="blog-about"),
    path("post/new_post/", views.create_post, name="new-post"),
    
    path("post/<int:pk>/post_delete/", views.delete_post, name="delete-post"),
    path("post/<int:pk>/post_edit/", views.edit_post, name="edit-post"),
    path("post/<int:pk>/<slug:slug>/", views.post_detail, name="post-detail"),

    # User route
    path("user/register/", views.user_registration, name="user-register"),
    path("user/login/", views.user_login, name="user-login"),
    path("user/logout/", views.user_logout, name="user-logout"),
    path("user/profile/", views.profile, name="profile"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="user/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="user/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="user/password_reset.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="user/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("post/like/", views.like_post, name="like-post"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
