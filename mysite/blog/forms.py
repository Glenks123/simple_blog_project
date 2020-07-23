from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):

    class Meta():
        #Connect to the model Post
        model = Post
        #Fields that I can edit
        fields = ('author','title','text',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','text',)
        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
        }
