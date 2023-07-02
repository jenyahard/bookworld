from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView
from django.views.generic import ListView, UpdateView

from book.forms import BookForm, CommentForm
from book.models import Author, Book, Comment
from book.services import paginator_custom
from book.forms import RegistrationForm


class IndexView(ListView):
    model = Book
    template_name = 'pages/index.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return Book.objects.filter(is_archived=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        books = (self.get_queryset()
                 .annotate(comment_count=Count('comment'))
                 .order_by('-id'))
        try:
            current_user = Author.objects.get(userdata=self.request.user)
            context['current_user_author_name'] = current_user
        except:
            pass
        context['page_obj'] = paginator_custom(self, books)
        return context


class ProfileView(DetailView):
    model = Book
    template_name = 'book/profile.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            author_id = self.kwargs['pk']
            author = Author.objects.get(userdata=author_id)
            current_user = Author.objects.get(userdata=request.user)
            self.extra_context = {
                'current_user_author_name': current_user,
                'author': author,
                'page_obj': paginator_custom(self, self.get_books(author))
            }
        except Author.DoesNotExist:
            return redirect('book:index')  # Выполняем перенаправление на 'book:index'

        return super().dispatch(request, *args, **kwargs)

    def get_books(self, author):
        return self.get_queryset().annotate(comment_count=Count('comment')).filter(
            author=author, is_archived=False).order_by('-id')




class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    context_object_name = 'page_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            current_user = self.request.user
            context['current_user_author_name'] = Author.objects.get(
                userdata=current_user)
        except:
            pass
        context['form'] = CommentForm()
        context['comments'] = (Comment.objects
                               .filter(book=self.object)
                               .order_by('-created_at')
                               )
        return context


class AuthorPostsView(ListView):
    model = Book
    paginate_by = 2
    template_name = 'book/profile.html'
    context_object_name = 'page_obj'


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'includes/comments.html'

    def get_success_url(self):
        return reverse_lazy('book:book_detail',
                            kwargs={'pk': self.kwargs['pk']}
                            )

    def form_valid(self, form):
        form.instance.author_id = self.request.user.author.id
        form.instance.book_id = self.kwargs['pk']
        return super().form_valid(form)


class EditCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'book/book_form.html'

    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse_lazy('book:book_detail',
                            kwargs={'pk': self.kwargs['post_id']}
                            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs['post_id']
        return context

    def form_valid(self, form):
        form.instance.author_id = self.request.user.author.id
        form.instance.id = self.kwargs['comment_id']
        form.instance.created_at = timezone.now()
        return super().form_valid(form)


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'book/post_confirm_delete.html'
    context_object_name = 'page_obj'
    
    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse_lazy('book:book_detail',
                            kwargs={'pk': self.kwargs['post_id']}
                            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            current_user = Author.objects.get(userdata=self.request.user)
            context['current_user_author_name'] = current_user
        except:
            pass
        return context


class AddBookView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_form.html'

    def get_success_url(self):
        return reverse_lazy('book:index')

    def form_valid(self, form):
        book = form.save(commit=False)
        book.save()
        book.author.set([self.request.user.id])
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_form.html'

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_success_url(self) -> str:
        return reverse_lazy('book:book_detail',
                            kwargs={'pk': self.object.id})


class BookDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('book:index')
    model = Book
    form_class = BookForm
    template_name = 'book/post_confirm_delete.html'
    context_object_name = 'page_obj'

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            current_user = Author.objects.get(userdata=self.request.user)
            context['current_user_author_name'] = current_user
        except:
            pass
        return context


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request,
                  'registration/registration_form.html',
                  {'form': form})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy('book:index')
    template_name = 'registration/registration_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = self.get_object()
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return super().form_valid(form)
