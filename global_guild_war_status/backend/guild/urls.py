from django.urls import path
from .views import global_guild_status,global_guild_form  # `fetch_global_global_guild_war_status` を削除

urlpatterns = [
    path('global_gvg_form/', global_guild_form, name='global_guild_form'),
    path("global_gvg_status/", global_guild_status, name="global_guild_status"),  # `global_guild_status` に変更
]
