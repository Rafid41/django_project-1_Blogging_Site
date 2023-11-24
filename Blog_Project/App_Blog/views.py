from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView, DeleteView
from App_Blog.models import Blog, Comment, Likes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid  # generate unique id
from App_Blog.forms import CommentForm

# Create your views here.


# mixins
# use hoy parameter hishebe
class CreateBlog( LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'App_Blog/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image',)

    #class based view te form submit er por kaj korbe:
    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user  # class er kisu use korte hole age "self." add korte hbe
        title = blog_obj.blog_title
        blog_obj.slug = str(title.replace(" ", "-")) + "-" + str(uuid.uuid4())   # uuid cz slug unique hote hbe, tai title jdi same hy, tar pore ektqa unique id lagiye dbe
        blog_obj.save()

        return HttpResponseRedirect(reverse('index'))
        
    

class BlogList(ListView):
    context_object_name = 'blogs'  # this 'blog' will be passed to html as dictionary
    model = Blog
    template_name = 'App_Blog/blog_list.html'

    # show last in top
    #queryset = Blog.objects.order_by('-publish_date')
    # NOTE: ascending sort : queryset = Blog.objects.order_by('publish_date')
    # descending sort : queryset = Blog.objects.order_by('-publish_date')
    # descending e 'field_name' er age minus sign (-) dte hbe
    # or models.py e giye edit kora jabe



@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)  
    # Select * from Blog where slug=slug
    # mane db er j slug amr slug er sathe mile jay seta nibo

    #liked or not chk
    already_liked = Likes.objects.filter(blog=blog, user=request.user)

    if already_liked:
        liked = True
    else:
        liked = False


    # comment
    comment_form = CommentForm(request.POST)


    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit= False)
            comment.user = request.user
            comment.blog = blog # current blog
            comment.save()

            return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug': slug})) 
            # kwargs pass cz in urls.py:
            # path('details/<slug:slug>/', views.blog_details, name='blog_details'),
            # etay <slug:slug> argument expect kore, ejnnoi slug send kora hoise


    return render(request, 'App_Blog/blog_details.html', context= {'blog': blog, 'comment_form': comment_form, 'liked': liked})



# like post
@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)  # cureent primary key pass kora holo
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    
    if not already_liked:
        liked_post = Likes(blog=blog, user=user)
        liked_post.save()

    return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs= {'slug': blog.slug}))


# unlike
@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user

    # like kora objects tanbe
    already_liked = Likes.objects.filter(blog=blog, user=user)

    #delete that obj
    already_liked.delete()

    return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs= {'slug': blog.slug}))


# show usrers own blog 
class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'App_Blog/my_blogs.html'




# update/edit blog
class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('blog_title', 'blog_content', 'blog_image')
    template_name = 'App_Blog/edit_blog.html'

    # update successful hole kon page e jabe
    # update and delete er khettre eta kora lage
    # must use reverse_lazy(), it will only if update is successful
    # kwargs used bcz 'blog_details' needs an additional argument
    def get_success_url(self, **kwargs):
        return reverse_lazy('App_Blog:blog_details', kwargs={'slug': self.object.slug})
    