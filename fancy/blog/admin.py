from django.contrib import admin
from models import Post, Category, PostMeta

class MetaInline(admin.TabularInline):
    model = PostMeta
    extra = 0

class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}

	list_display = ('title','date','status')
	list_filter = ['date']
	list_editable = ('date',)
	search_fields = ['title']
	date_hierarchy = 'date'
	inlines = [MetaInline]

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	
admin.site.register(Post,PostAdmin)
admin.site.register(Category,CategoryAdmin)