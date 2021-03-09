from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Comment # model 
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator # pagination 
from .forms import EmailForms,CommentForm # form
from django.core.mail import send_mail # this is for Email sending by django 
from taggit.models import Tag # for tag 
from django.db.models import Count 
# Create your views here.
#...................................=================================...................................................

def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in = [tag])
    pagenator = Paginator(posts,3) # each page have 3 post only 
    page = request.GET.get('page')   # it's indicate us the current page number 
    try:
        postes = pagenator.page(page)
    except PageNotAnInteger:
        postes = pagenator.page(1) # if the page is not intiger we will get the first page in blog 
    except EmptyPage:
        postes = pagenator.page(pagenator.num_pages) # jodi kono page na thake tahole amra last page dakhte pabo    
    
    context = {
        'posts':posts,
        'page':page,
        'posts':postes,
        'tag':tag,
    }
    return render(request, 'Home.html', context)
#..........................>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>...............................

def post_details(request, year, month, day, post):
    post = get_object_or_404(Post, slug = post, status = 'published', publish__year=year, publish__month= month, publish__day=day)
    comments = post.comments.filter(active = True) 
    new_comment = None 
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            # return redirect("blog:Post") 
    else:
        comment_form = CommentForm()    
    
    post_tag_ids = post.tags.values_list('id', flat = True)
    similar_post = Post.published.filter(tags__in = post_tag_ids) \
                    .exclude(id=post.id)
    similar_post = similar_post.annotate(same_tags = Count('tags')) \
                .order_by('-same_tags','-publish')[:4]
    context = {
        'post':post,
        'comments':comments, # all comment 
        'new_comment':new_comment, # new commet is passing 
        'comment_form':comment_form, # comment form 
        'similar_post':similar_post,
        
        
    }
    return render(request, 'PostDetails.html',context)
#...................................>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..............................................................

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST': 
        #form is submitted 
        form = EmailForms(request.POST)
        if form.is_valid():
            # form is validatted now
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            
            subject = f"{cd['name']} recommends you read" \
                f"{post.title}"
            message = f" Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments : {cd['comment']}"
            send_mail(subject, message, 'jimnill93225@gmail.com', [cd['to']])
            sent = True
        # return redirect("blog:Post")        
            
    else:
        form = EmailForms()        
    
    context = {
        'post':post,
        'form':form,
        'sent':sent
    }
    return render(request, 'share.html', context)
      