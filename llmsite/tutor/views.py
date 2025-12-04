# llmsite/tutor/views.py

#import profile
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm
import json

from languagemodel import StartAIChat, Initialization, SendMessage
from .models import Session, Chat as DBChat

# in-memory registry for prototype use
CHAT_REGISTRY = {}

def _session_id(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key

def chat_page(request):
    return render(request, "chat.html")

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def api_new_session(request):
    """Create a new Session for the authenticated user and return its metadata."""
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    title = (data.get("title") or "New session").strip() or "New session"
    session = Session.objects.create(owner=request.user, title=title)

    # store the session id in the user's django session to aid backwards compatibility
    request.session["session_id"] = str(session.id)

    return JsonResponse({
        "ok": True,
        "id": str(session.id),
        "title": session.title,
        "createdAt": session.created_at.isoformat(),
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_init(request):
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "error": "authentication required"}, status=401)

    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    session_id = data.get("session_id")
    if not session_id:
        return HttpResponseBadRequest("Session ID is required")

    try:
        session = Session.objects.get(id=session_id, owner=request.user)
    except Session.DoesNotExist:
        return HttpResponseBadRequest("Session not found or not owned by user")

    # Use profile info
    try:
        profile = request.user.studentprofile
        name = profile.user.get_full_name() or profile.user.username
        school = profile.school
        grade = profile.grade
        classes = profile.classes
    except Exception:
        name = request.user.get_full_name() or request.user.username
        school = ""
        grade = ""
        classes = ""

    # Start chat only once per session
    llm_chat = CHAT_REGISTRY.get(session_id)
    if not llm_chat:
        llm_chat = StartAIChat()
        CHAT_REGISTRY[str(session_id)] = llm_chat

    # Initialize LLM
    init_text = Initialization(llm_chat, name, school, grade, classes) or ""

    # Persist initial assistant message if not already present
    if not DBChat.objects.filter(session=session, role="assistant").exists():
        DBChat.objects.create(session=session, role="assistant", message=init_text)

    return JsonResponse({"ok": True, "model_text": init_text})



@csrf_exempt
@require_http_methods(["POST"])
@login_required
def api_chat(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    msg = (data.get("message") or "").strip()
    session_id = data.get("session_id")
    if not msg:
        return HttpResponseBadRequest("Message is required")
    if not session_id:
        return HttpResponseBadRequest("Session ID is required")

    # Ensure session exists and belongs to user
    try:
        session = Session.objects.get(id=session_id, owner=request.user)
    except Session.DoesNotExist:
        return HttpResponseBadRequest("Session not found or not owned by user")

    # Look up the live chat in memory; if missing, initialize it here
    chat = CHAT_REGISTRY.get(str(session_id))
    if chat is None:
        # create and initialize using the user's profile (same logic as api_init)
        chat = StartAIChat()
        CHAT_REGISTRY[str(session_id)] = chat

        try:
            profile = request.user.studentprofile
            name = profile.user.get_full_name() or profile.user.username
            school = profile.school
            grade = profile.grade
            classes = profile.classes
        except Exception:
            name = request.user.get_full_name() or request.user.username
            school = ""
            grade = ""
            classes = ""

        init_text = Initialization(chat, name, school, grade, classes) or ""
        # persist initial assistant message if not present
        try:
            if not DBChat.objects.filter(session=session, role="assistant").exists():
                DBChat.objects.create(session=session, role="assistant", message=init_text)
        except Exception:
            # ignore DB errors but continue
            pass

    # Send the user message to the LLM
    reply = SendMessage(chat, msg) or ""

    # Save messages in DB (user + assistant)
    try:
        DBChat.objects.create(session=session, role="user", message=msg)
        DBChat.objects.create(session=session, role="assistant", message=reply)
    except Exception:
        pass

    return JsonResponse({"ok": True, "model_text": reply})



@csrf_exempt
@require_http_methods(["POST"])
def api_reset(request):
    sid = _session_id(request)
    CHAT_REGISTRY.pop(sid, None)
    return JsonResponse({"ok": True})

@login_required
def api_list_sessions(request):
    """Return all sessions for the current user."""
    sessions = Session.objects.filter(owner=request.user).order_by("-created_at")
    data = [
        {"id": str(s.id), "title": s.title, "created_at": s.created_at.isoformat()}
        for s in sessions
    ]
    return JsonResponse({"sessions": data})


@login_required
@require_GET
def api_session_messages(request, session_id):
    try:
        session = Session.objects.get(id=session_id, owner=request.user)
    except Session.DoesNotExist:
        return HttpResponseBadRequest("Session not found or not owned by user")

    chats = DBChat.objects.filter(session=session)
    messages = [{"role": c.role, "text": c.message} for c in chats]

    return JsonResponse({"ok": True, "messages": messages})

@csrf_exempt
@require_http_methods(["DELETE"])
@login_required
def api_delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id, owner=request.user)
    # remove in-memory chat if present
    CHAT_REGISTRY.pop(str(session_id), None)
    session.delete()
    return JsonResponse({"ok": True, "status": "deleted"})


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def api_rename_session(request, session_id):
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")
    new_title = (data.get("title") or "").strip()
    if not new_title:
        return HttpResponseBadRequest("title is required")
    session = get_object_or_404(Session, id=session_id, owner=request.user)
    session.title = new_title
    session.save(update_fields=["title"])
    return JsonResponse({"ok": True, "id": str(session.id), "title": session.title})

