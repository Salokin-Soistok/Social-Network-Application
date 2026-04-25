from django.shortcuts import render, redirect, get_object_or_404  # Import necessary shortcuts for views
from django.db.models import Q  # Import Q for complex queries
from django.urls import reverse_lazy  # Import for URL reversal
from django.http import HttpResponseRedirect  # Import for HTTP redirects
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin  # Import mixins for user authentication
from django.views import View  # Import base view class
from .models import Post, Comment, UserProfile  # Import models used in the views
from .forms import PostForm, CommentForm  # Import forms used in the views
from django.views.generic.edit import UpdateView, DeleteView  # Import generic views for editing and deleting

# View to list all posts and handle new post creation
class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')  # Retrieve all posts ordered by creation date
        form = PostForm()  # Instantiate the post form

        context = {
            'post_list': posts,  # Include the list of posts in the context
            'form': form,  # Include the form in the context
        }

        return render(request, 'social/post_list.html', context)  # Render the post list template with context

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')  # Retrieve all posts ordered by creation date
        form = PostForm(request.POST)  # Bind the form to the submitted data

        if form.is_valid():  # Check if the form is valid
            new_post = form.save(commit=False)  # Create a post instance without saving to the database yet
            new_post.author = request.user  # Set the author to the current user
            new_post.save()  # Save the new post to the database

        context = {
            'post_list': posts,  # Include the list of posts in the context
            'form': form,  # Include the form in the context
        }

        return render(request, 'social/post_list.html', context)  # Render the post list template with context

# View to display a single post and its comments
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)  # Retrieve a specific post by primary key
        form = CommentForm()  # Instantiate the comment form

        comments = Comment.objects.filter(post=post).order_by('-created_on')  # Retrieve comments for the post

        context = {
            'post': post,  # Include the post in the context
            'form': form,  # Include the comment form in the context
            'comments': comments,  # Include the comments in the context
        }

        return render(request, 'social/post_detail.html', context)  # Render the post detail template with context

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)  # Retrieve the post
        form = CommentForm(request.POST)  # Bind the form to the submitted data

        if form.is_valid():  # Check if the form is valid
            new_comment = form.save(commit=False)  # Create a comment instance without saving to the database yet
            new_comment.author = request.user  # Set the author to the current user
            new_comment.post = post  # Associate the comment with the post
            new_comment.save()  # Save the new comment to the database

        comments = Comment.objects.filter(post=post).order_by('-created_on')  # Retrieve updated comments

        context = {
            'post': post,  # Include the post in the context
            'form': form,  # Include the comment form in the context
            'comments': comments,  # Include the comments in the context
        }

        return render(request, 'social/post_detail.html', context)  # Render the post detail template with context

# View to edit an existing post
class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post  # Specify the model to edit
    fields = ['body']  # Specify fields to include in the form
    template_name = 'social/post_edit.html'  # Specify the template for editing

    def get_success_url(self):
        pk = self.kwargs['pk']  # Get the post's primary key from URL
        return reverse_lazy('post-detail', kwargs={'pk': pk})  # Redirect to the post detail page

    def test_func(self):
        post = self.get_object()  # Get the post object
        return self.request.user == post.author  # Ensure only the author can edit the post

# View to delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post  # Specify the model to delete
    template_name = 'social/post_delete.html'  # Specify the template for deletion
    success_url = reverse_lazy('post-list')  # Redirect to the post list after deletion

    def test_func(self):
        post = self.get_object()  # Get the post object
        return self.request.user == post.author  # Ensure only the author can delete the post

# View to delete a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment  # Specify the model to delete
    template_name = 'social/comment_delete.html'  # Specify the template for deletion

    def get_success_url(self):
        pk = self.kwargs['post_pk']  # Get the post's primary key from URL
        return reverse_lazy('post-detail', kwargs={'pk': pk})  # Redirect to the post detail page

    def test_func(self):
        post = self.get_object()  # Get the comment object
        return self.request.user == post.author  # Ensure only the author can delete the comment

# View to display a user's profile
class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)  # Retrieve the user profile
        user = profile.user  # Get the user associated with the profile
        posts = Post.objects.filter(author=user).order_by('-created_on')  # Retrieve posts by the user

        followers = profile.followers.all()  # Get the list of followers

        is_following = request.user in followers  # Check if the current user is following

        context = {
            'user': user,  # Include the user in the context
            'profile': profile,  # Include the profile in the context
            'posts': posts,  # Include the user's posts in the context
            'number_of_followers': followers.count(),  # Count followers for display
            'is_following': is_following,  # Include follow status in the context
        }

        return render(request, 'social/profile.html', context)  # Render the profile template with context

# View to edit a user's profile
class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile  # Specify the model to edit
    fields = ['name', 'bio', 'birth_date', 'location', 'picture']  # Specify fields to include in the form
    template_name = 'social/profile_edit.html'  # Specify the template for editing

    def get_success_url(self):
        pk = self.kwargs['pk']  # Get the profile's primary key from URL
        return reverse_lazy('profile', kwargs={'pk': pk})  # Redirect to the profile page

    def test_func(self):
        profile = self.get_object()  # Get the user profile object
        return self.request.user == profile.user  # Ensure only the profile owner can edit

# View to add a follower
class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)  # Retrieve the user profile
        profile.followers.add(request.user)  # Add the current user as a follower
        return redirect('profile', pk=profile.pk)  # Redirect to the profile page

# View to remove a follower
class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)  # Retrieve the user profile
        profile.followers.remove(request.user)  # Remove the current user as a follower
        return redirect('profile', pk=profile.pk)  # Redirect to the profile page

# View to add or remove a like on a post
class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)  # Retrieve the post
        is_dislike = request.user in post.dislikes.all()  # Check if the user has disliked the post
        
        if is_dislike:  # If the user has disliked the post
            post.dislikes.remove(request.user)  # Remove the dislike

        is_like = request.user in post.likes.all()  # Check if the user has liked the post
        if not is_like:  # If the user has not liked the post
            post.likes.add(request.user)  # Add the like
        else:  # If the user has liked the post
            post.likes.remove(request.user)  # Remove the like

        next_url = request.POST.get('next', '/')  # Get the next URL to redirect to
        return HttpResponseRedirect(next_url)  # Redirect to the next URL

# View to add or remove a dislike on a post
class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)  # Retrieve the post
        is_like = request.user in post.likes.all()  # Check if the user has liked the post
        
        if is_like:  # If the user has liked the post
            post.likes.remove(request.user)  # Remove the like

        is_dislike = request.user in post.dislikes.all()  # Check if the user has disliked the post
        if not is_dislike:  # If the user has not disliked the post
            post.dislikes.add(request.user)  # Add the dislike
        else:  # If the user has disliked the post
            post.dislikes.remove(request.user)  # Remove the dislike

        next_url = request.POST.get('next', '/')  # Get the next URL to redirect to
        return HttpResponseRedirect(next_url)  # Redirect to the next URL

# View to search for users
class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query', '')  # Get the search query from GET parameters
        profile_list = UserProfile.objects.filter(  # Filter user profiles based on the search query
            Q(user__username__icontains=query)  # Match usernames that contain the query
        )

        context = {
            'profile_list': profile_list,  # Include the list of user profiles in the context
        }

        return render(request, 'social/search.html', context)  # Render the search results template with context
