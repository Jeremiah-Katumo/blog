from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

from . import models
from . import forms


# Using the generic ListView
class PostListView(ListView):
    """Alternative post list view"""
    queryset = models.Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blogsite/post/list.html'

# Create your views here.
def post_list(request):
    post_list = models.Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    template = loader.get_template('list.html')
    context = {
        'posts': posts
    }

    return HttpResponse(template.render(context, request))

def post_detail(request, year, month, day, post):
    post = get_object_or_404(models.Post,
        status=models.Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    
    template = loader.get_template('detail.html')
    context = {
        'post': post
    }

    return HttpResponse(template.render(context, request))
    # try:
    #     post = models.Post.published.get(id=id)
    #     template = loader.get_template('detail.html')
    #     context = {
    #         'post_detail': post
    #     }
    # except models.Post.DoesNotExist:
    #     raise Http404("No post found")
    # return HttpResponse(template.render(context, request))


def post_share(request, post_id):
    post = get_object_or_404(models.Post, id=post_id, status=models.Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = forms.EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends reading '{post.title}'"
            message = f"Read '{post.title}' at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'noreply@example.com', [cd['email']])
            sent = True
    else:
        form = forms.EmailPostForm()
        context = {
            'post': post,
            'form': form,
            'sent': sent,
        }

    return render(request, 'blogsite/post/share.html', context)
    # send email or other sharing logic here
    # return HttpResponseRedirect(post.get_absolute_url())