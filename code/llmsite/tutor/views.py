from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from languagemodel import StartChat, SendMessage
from manage import GetModelAndTokenizer

# in-memory registry for prototype use
CHAT_REGISTRY = {}

model, tokenizer = GetModelAndTokenizer()

def _session_id(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key

def chat_page(request):
    return render(request, "chat.html")

@csrf_exempt
@require_http_methods(["POST"])
def api_init(request):
    #try:
        #data = json.loads(request.body.decode("utf-8"))
    #except Exception:
        #return HttpResponseBadRequest("Invalid JSON")

    name   = "John Doe" #(data.get("studentName") or "").strip()
    school = "George Washington High School" #(data.get("studentSchool") or "").strip()
    grade  = "Sophomore" #(data.get("studentGrade") or "").strip()
    classes = "Algebra 2, History, AP Language/Composition" #(data.get("studentClasses") or "").strip()

    # Initialize the chat.
    # TODO: Retreive chats and RAG from database.
    chat = StartChat(model, tokenizer, name, school, grade, classes)

    # store the live chat object for this user session
    sid = _session_id(request)
    CHAT_REGISTRY[sid] = chat

    model_reply = chat.split("<|assistant|>").strip()

    return JsonResponse({"ok": True, "model_text": model_reply})

@csrf_exempt
@require_http_methods(["POST"])
def api_chat(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    msg = (data.get("message") or "").strip()
    if not msg:
        return HttpResponseBadRequest("message is required")

    sid = _session_id(request)
    chat = CHAT_REGISTRY.get(sid)
    if chat is None:
        return HttpResponseBadRequest("No active chat, initialize first")

    # call SendMessage on the stored chat
    CHAT_REGISTRY[sid] = SendMessage(model, tokenizer, chat, msg)
    model_reply = CHAT_REGISTRY.get(sid).split("<|assistant|>").strip()
    
    return JsonResponse({"ok": True, "model_text": model_reply})

@csrf_exempt
@require_http_methods(["POST"])
def api_reset(request):
    sid = _session_id(request)
    CHAT_REGISTRY.pop(sid, None)
    return JsonResponse({"ok": True})
