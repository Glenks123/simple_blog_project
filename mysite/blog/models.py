from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

# Create your models here.
class Post(models.Model):
    #Since the project is only for a single user, we are using auth.User so that only the authorised person can post something
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comments=True)

    def get_absolute_url(self):
        #After we finish writing the post, it takes us back to the page where we wrote out post.
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments')
    #Here author means who wrote the comment, not the writer of the blog
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comments = models.BooleanField(default=False)

    def approve(self):
        self.approved_comments = True
        self.save()

    def get_absolute_url(self):
        #After we write our post, we get redirected to the list of posts page
        return reverse('post_list')

    def __str__(self):
        return self.text
