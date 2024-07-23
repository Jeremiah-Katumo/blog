from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from . import models

# Create your views here.
def post_list(request):
    posts = models.Post.published.all()
    template = loader.get_template('list.html')
    context = {
        'posts': posts
    }
    return HttpResponse(template.render(context, request))

def post_detail(request):
    # post = get_object_or_404(models.Post,
    #     id=id,
    #     status=models.Post.Status.PUBLISHED)
    try:
        post = models.Post.published.get(id=id)
        template = loader.get_template('detail.html')
        context = {
            'post_detail': post
        }
    except models.Post.DoesNotExist:
        raise Http404("No post found")

    return HttpResponse(template.render(context, request))