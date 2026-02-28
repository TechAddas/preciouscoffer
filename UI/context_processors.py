from .models import SiteSocialLinks


def site_social_links(request):
    return {
        "site_social_links": SiteSocialLinks.objects.first(),
    }
