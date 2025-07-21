from django.conf import settings
from django.db import models
from django.utils import timezone

class Topic(models.Model):
    
    name = models.CharField(
        max_length=50,
        unique = True
    )
    
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=self.model.PUBLISHED)
    
    def draft(self):
        return self.filter(status=self.model.DRAFT)
    
class Post(models.Model):
    """
    Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]
    
    title = models.CharField(max_length=255)
    
    slug = models.SlugField(
        null = False,
        unique_for_date = 'published',
    )
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.PROTECT,
        related_name = 'blog_posts',
        null = False,
    )
    status = models.CharField(
        max_length = 10,
        choices = STATUS_CHOICES,
        default = DRAFT,
        help_text = 'Set to "published" to make this post publicly visible',
    )
    topics = models.ManyToManyField(
        Topic,
        related_name = 'blog_posts'
    )
    
    content = models.TextField()
    published = models.DateTimeField(
        null = True,
        blank = True,
        help_text = 'The date & time this article was published'
    )
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    prepopulated_fields = {'slug':('title,')}
    
    def publish(self):
        self.status = self.PUBLISHED
        self.published = timezone.now()
    
    class Meta:
        """
        sort by the 'created' field. The '-' prefix
        specifies to order in descending/reverse order. Otherwise, it will be in ascending order.
        """
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    
    objects = PostQuerySet.as_manager()

