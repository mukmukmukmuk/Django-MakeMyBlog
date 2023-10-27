from django.views.generic import ListView,DetailView
from .models import Post,Category
from django.shortcuts import render
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

'''
def single_post_page(request,pk):
    post=Post.objects.get(pk=pk)
    return render(
        request,
        'blog/post_detail.html',
        {
            'post':post
        }
    )
'''