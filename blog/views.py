from typing import Any
from django import http
from django.http.response import HttpResponse
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from .models import Post,Category,Tag,Comment
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify


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
            response=super().form_valid(form)

            tags=self.request.POST.get('tags')
            if tags:
                tags_list = tags.strip().replace(',',';').split(';')
                for t in tags_list:
                    t=t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug=slugify(t,allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/blog/')
    
class PostUpdate(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['title','hook_text','content','head_image','file_upload','category']

    template_name='blog/post_update_form.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data()
        if self.object.tags.exists():
            context['tags_str_default']= '; '.join([t.name for t in self.object.tags.all()])
        return context

    def dispatch(self,request, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
        
    def form_valid(self, form):
        response=super().form_valid(form)
        self.object.tags.clear()
        tags=self.request.POST.get('tags')
        if tags:
            tags_list = tags.strip().replace(',',';').split(';')
            for t in tags_list:
                t=t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug=slugify(t,allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response