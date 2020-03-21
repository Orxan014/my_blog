from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey("auth.User", verbose_name='Müəllif', on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(verbose_name='Başlıq',max_length=50)
    content = RichTextField(verbose_name ='Mətn')
    publishing_date = models.DateTimeField(verbose_name='Yazılma tarixi',auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(unique=True, editable=False, max_length=80)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'slug': self.slug})


    def get_create_url(self):
        return reverse("post:create")


    def get_update_url(self):
        return reverse("post:update", kwargs={"slug": self.slug})


    def get_delete_url(self):
        return reverse("post:delete", kwargs={"slug": self.slug})


    def unique_slug(self):
        slug = slugify(self.title.replace('ə','e'))
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug,counter)
            counter += 1
        return unique_slug


    def save(self,*args,**kwargs):
        self.slug = self.unique_slug()
        return super(Post,self).save(*args,**kwargs)

    class Meta:
        ordering = ['-publishing_date']




class Comment(models.Model):
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(verbose_name='Ad', max_length = 250)
    content = models.TextField(verbose_name='Rəy', max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)