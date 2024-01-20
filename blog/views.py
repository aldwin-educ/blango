from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from blog.models import Post
from blog.forms import CommentForm

#from django.views.decorators.cache import cache_page
#from django.views.decorators.vary import vary_on_cookie

import logging
logger = logging.getLogger(__name__)

#@cache_page(300)
#@vary_on_cookie
def index(request):
    #from django.http import HttpResponse
    #logger.debug("Index function is called!") # you should only see this the first time since subsequent functiokn call is not performed.  Or wait 5 mins
    #return HttpResponse(str(request.user).encode("ascii"))

    posts = Post.objects.filter(published_at__lte=timezone.now())
    logger.debug("Got %d posts", len(posts))
    
    return render(request, "blog/index.html", {"posts": posts})

def post_detail(request, slug):

    post=get_object_or_404(Post,slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                logger.info(
    "Created comment on Post %d for user %s", post.pk, request.user
)
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None

    
    return render(
        request, "blog/post_detail_with_form.html", {"post": post, "comment_form": comment_form}
    )    