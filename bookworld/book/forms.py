from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from book.models import Author, Book, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class RegistrationForm(UserCreationForm):
    author_name = forms.CharField(label='Имя автора книги для отображения на сайте')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'author_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        author_name = self.cleaned_data['author_name']
        author, created = Author.objects.get_or_create(userdata=user)
        author.author_name = author_name
        author.save()

        return user 