from django.views.generic import ListView,DetailView,CreateView
from .models import Post,Category,Tag
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
#def index(request):
#    posts=Post.objects.all().order_by('-pk')
#    return render(
#        request,
#        'blog/post_list.html',
#        {
#            'posts':posts,
#
#        }
#    )

def category_page(request,slug):
    if slug=='no_category':
        category = '미분류'
        post_list=Post.objects.filter(category=None)
    else:
        category=Category.objects.get(slug=slug)
        post_list=Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories':Category.objects.all(),
            'no_category_post_count':Post.objects.filter(category=None).count(),
            'category':category,
        }
    )

def tag_page(request,slug):
    tag=Tag.objects.get(slug=slug)
    post_list=tag.post_set.all()
    #post_list=Post.objects.filter(tags=tag)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list,
            'tag' : tag,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
        }
    )

class PostList(ListView):
    model=Post
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model=Post
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostCreate(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model=Post
    fields=['title','hook_text','content','head_image','file_upload','category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user=self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super().form_valid(form)
        else:
            return redirect('/blog/')
    