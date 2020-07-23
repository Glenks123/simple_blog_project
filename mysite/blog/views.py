from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from blog.models import Comment,Post
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    #We are writing model=Post because we are using the values and other things
    model = Post

    def get_queryset(self):
        #It orders a list of all the posts from newest to oldest
        #published_date__lte=timezone.now(), orders it according to the time which is oldest to newest.
        #But, we want to see the newest at the top, so order_by('-published_date') does exactly  that
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

#Since @login_required doesnt work for classes, only for functions, we have to import LoginRequiredMixin
class CreatePostView(LoginRequiredMixin,CreateView):
    #Since we added LoginRequiredMixin, we need to add in some extra UserAttributeSimilarityValidator
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
#________________________________________________________________________________________________#

class PostUpdateView(LoginRequiredMixin,UpdateView):
    #We can just copy and paste those same attributes
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):

    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


#####################################################################
#####################################################################
#####################################################################

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        #If they user did not add a comments
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})
    #I am going to the context dictionary form, to comment_form

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    #Here we are calling the approve functions from the models, so the boolean value changes from False to True
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_delete(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)
