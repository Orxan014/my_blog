from django.shortcuts import render,Http404, HttpResponse, get_object_or_404, HttpResponseRedirect,redirect
from .models import Post
from .forms import *
from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


# Create your views here.




def post_index(request):
    post_var = Post.objects.all() #Post objeclerini post_var deyisenine menimsetdik
    query = request.GET.get('q')
    if query:
        post_var = post_var.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()



    paginator = Paginator(post_var, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, "post/index.html", {'posts': posts})



def post_detail(request,slug):
    spec_post = get_object_or_404(Post, slug=slug)
    form_var = CommentForm(request.POST or None, request.FILES or None)
    if form_var.is_valid():
        comment_here = form_var.save(commit=False) # save metodundan qayidan objecti stored_form deyiseninde saxladiq
        comment_here.post = spec_post
        comment_here.save()
        return HttpResponseRedirect(spec_post.get_absolute_url())
        
    context = {
        'post_det':spec_post,
        'form':form_var,
    }
    return render(request, 'post/detail.html', context)






def post_create(request):
    if not request.user.is_authenticated:
        raise Http404()

    form_var = PostForm(request.POST or None, request.FILES or None)
    if form_var.is_valid():
        stored_form = form_var.save(commit=False) # save metodundan qayidan objecti stored_form deyiseninde saxladiq
        stored_form.user = request.user
        stored_form.save()

        messages.success(request, 'Məqaləniz dərc olundu')
        return HttpResponseRedirect(stored_form.get_absolute_url())

    context = {
        'form': form_var
    }

    return render(request, "post/form.html", context)




def post_update(request,slug):
    if not request.user.is_authenticated:
        raise Http404()
    spec_post = get_object_or_404(Post, slug=slug) #
    form_var = PostForm(request.POST or None,request.FILES or None, instance=spec_post)
    if form_var.is_valid():
        form_var.save()
        messages.success(request,'Məqalənizdə dəyişiklik edildi')

        return HttpResponseRedirect(spec_post.get_absolute_url())
    context = {
    'form':form_var,
}
    return render(request,'post/form.html',context)






def post_delete(request,slug):
    if not request.user.is_authenticated:
        raise Http404()
    spec_post = get_object_or_404(Post, slug=slug)
    spec_post.delete()
    return redirect('post:index')
