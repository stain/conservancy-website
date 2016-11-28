from conservancy import render_template_with_context
from conservancy.apps.blog.models import Entry as BlogEntry
from datetime import datetime

def index(request):
    filters = {
        'pub_date__lte': datetime.now(),
        'tags__slug': 'ContractPatch',
    }
    context = {
        'blog_entries': BlogEntry.objects.filter(**filters)[:3],
    }
    return render_template_with_context(request, "contractpatch/index.html", context)
