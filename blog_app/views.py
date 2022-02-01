from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import Post, Category, Profile
from .forms import SignUpForm, EditProfileForm, CreateProfileForm, UpdateProfileForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.


class HomeView(generic.ListView):
    template_name = 'home/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(title__icontains=query)
        return Post.objects.all()


class PostDetailView(generic.DetailView):
    queryset = Post.objects.all()
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    lookup_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        check_total_likes = get_object_or_404(Post, slug=self.kwargs['slug'])
        total_likes = check_total_likes.total_likes()
        context['total_likes'] = total_likes
        return context


class CreatePost(generic.CreateView):
    queryset = Post.objects.all()
    template_name = 'posts/create_post.html'
    fields = ['category', 'title', 'content', 'image']
    success_url = reverse_lazy('blog_app:home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePost(generic.UpdateView):
    queryset = Post.objects.all()
    template_name = 'posts/update_post.html'
    fields = ['category', 'title', 'content', 'image']
    success_url = reverse_lazy('blog_app:home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def delete_post(request, slug):
    post = Post.objects.get(slug=slug)
    if request.user == post.author:
        post.delete()
        return redirect('login')
    return redirect('blog_app:home')


class CreateCategory(generic.CreateView):
    queryset = Category.objects.all()
    template_name = 'categories/create_category.html'
    fields = ['name']
    success_url = reverse_lazy('blog_app:home')


def post_by_category(request, slug):
    category = Category.objects.get(slug=slug)
    posts = Post.objects.filter(category=category)
    context = {'category': category, 'posts': posts}
    return render(request, 'categories/post_by_category.html', context)


@login_required
def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        if post.liked.filter(id=user.id).exists():
            post.liked.remove(user)
        else:
            post.liked.add(user)
        return redirect('blog_app:post_detail', slug=post.slug)

    return redirect('blog_app:home')


class RegisterUserView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class UpdateUserView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('blog_app:home')

    def get_object(self):
        return self.request.user


class UpdatePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change-password.html'
    success_url = reverse_lazy('blog_app:home')

    def get_object(self):
        return self.request.user


def create_user_profile(request):
    if request.method == 'POST':
        form = CreateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('blog_app:home')
    else:
        form = CreateProfileForm()
    return render(request, 'registration/create_profile.html', {'form': form})


class UserProfileView(generic.DetailView):
    template_name = 'users/user_profile.html'
    context_object_name = 'profile'
    model = Profile

    def get_object(self, **kwargs):
        return get_object_or_404(Profile, user=self.request.user)


class UpdateProfileView(generic.UpdateView):
    queryset = Profile.objects.all()
    template_name = 'registration/update_profile.html'
    form_class = UpdateProfileForm
    success_url = reverse_lazy('blog_app:home')

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


class AddNewComment(generic.CreateView):
    form_class = CommentForm
    template_name = 'posts/add_comment.html'
    success_url = reverse_lazy('blog_app:home')
    lookup_field = 'slug'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(slug=self.kwargs['slug'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(slug=self.kwargs['slug'])
        return context
