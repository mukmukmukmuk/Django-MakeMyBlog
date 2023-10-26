from django.views.generic import ListView,DetailView
from .models import Post,Category

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