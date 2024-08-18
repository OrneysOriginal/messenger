from datetime import datetime
import asyncio

from typing import AsyncGenerator
from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, StreamingHttpResponse, HttpResponse
import json
from message.models import Messages, Author


def lobby(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            request.session['username'] = username
            return redirect(reverse('chat:chat'))
    return render(request, 'chat/lobby.html')


def chat(request: HttpRequest) -> HttpResponse:
    if not request.session.get('username'):
        return redirect(reverse('chat:lobby'))
    return render(request, 'chat/chat.html')


def create_message(request: HttpRequest) -> HttpResponse:
    content = request.POST.get("content")
    username = request.session.get("username")

    if not username:
        return HttpResponse(status=403)
    author, _ = Author.objects.get_or_create(username=username)

    if content:
        Messages.objects.create(author=author, content=content)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=200)


async def stream_chat_messages(request: HttpRequest) -> StreamingHttpResponse:
    async def event_stream():
        async for message in get_existing_messages():
            yield message
        last_id = await get_last_message_id()
        while True:
            new_messages = Messages.objects.filter(id__gt=last_id).order_by('created_at').values(
                'id', 'author__username', 'content'
            )
            async for message in new_messages:
                yield f"data: {json.dumps(message)}\n\n"
                last_id = message['id']
            await asyncio.sleep(0.1)

    async def get_existing_messages() -> AsyncGenerator:
        messages = Messages.objects.all().order_by('created_at').values(
            'id', 'author__username', 'content'
        )
        async for message in messages:
            yield f"data: {json.dumps(message)}\n\n"

    async def get_last_message_id() -> int:
        last_message = await Messages.objects.all().alast()
        return last_message.id if last_message else 0

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

