# llmsite/tutor/urls.py
from django.urls import path
from .views import chat_page, api_init, api_chat, api_reset, api_new_session, signup, api_list_sessions, api_session_messages, api_delete_session, api_rename_session

urlpatterns = [
    path("", chat_page, name="chat_page"),
    path("chat/", chat_page, name="chat_page"),
    path("signup/", signup, name="signup"),
    path("api/init/", api_init, name="api_init"),
    path("api/session/new/", api_new_session, name="api_new_session"),
    path("api/chat/", api_chat, name="api_chat"),
    path("api/reset/", api_reset, name="api_reset"),
    path("api/sessions/", api_list_sessions, name="api_list_sessions"),
    path("api/session/<uuid:session_id>/messages/", api_session_messages, name="api_session_messages"),
    path("api/session/<uuid:session_id>/delete/", api_delete_session, name="api_delete_session"),
    path("api/session/<uuid:session_id>/rename/", api_rename_session, name="api_rename_session")
]