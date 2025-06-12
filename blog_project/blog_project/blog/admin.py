from django.contrib import admin
from .models import Post, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'content')
    inlines = [CommentInline]
    actions = ['approve_posts', 'reject_posts']
    
    def approve_posts(self, request, queryset):
        queryset.update(status='published')
    approve_posts.short_description = "Approve selected posts"
    
    def reject_posts(self, request, queryset):
        queryset.update(status='rejected')
    reject_posts.short_description = "Reject selected posts"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'post', 'created_at')
    search_fields = ('content', 'user__username')