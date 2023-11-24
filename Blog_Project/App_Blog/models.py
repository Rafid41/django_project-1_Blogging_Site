from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name='post_author')
    blog_title = models.CharField(max_length=264, verbose_name="Put a Title") # verbose_name holo label er name
    slug = models.SlugField(max_length=264, unique=True)
    blog_content = models.TextField(verbose_name="What is on your mind?")
    blog_image = models.ImageField(upload_to='blog_images', verbose_name='Image')
    publish_date = models.DateTimeField(auto_now_add=True)   # auto current time nia nibe, user kisu korte parbena, only first entry nibe
    update_date = models.DateTimeField(auto_now=True) # auto current time nibe, but last entry er


    # show blog as descending order of publish date
    class Meta:
        ordering = ['-publish_date',]   
        # ascending hole just  ordering =  ['-publish_date',]
        # list or tuple:  ordering = ['-publish_date',] or, ordering = ('-publish_date',)



    def __str__(self):
        return self.blog_title
    
    '''
    slug filed holo, url e primary key pass orbe, eta na dekhaya blog title pass kora dekhay
    jate kore blog url dekhle amra title bujhte pari

    title er moddhe hiphen diye link kora hy

    like: www.newspaper.com/last-night-accident/
    '''

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete= models.CASCADE, related_name='blog_comment')
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='user_comment')
    comment=  models.TextField()
    comment_date= models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('-comment_date',)   # list or tuple


    def __str__(self):
        return self.comment
    


class Likes(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='liked_blog')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker_user')

    def __str__(self):
        return self.user + " likes " + self.blog