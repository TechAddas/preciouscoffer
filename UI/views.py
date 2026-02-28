from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Project, ProjectCategory, ProjectImage

def home(request):
    base_project_details_url = reverse("project-details")
    project_ids = list(
        Project.objects.order_by("-add_project_to_feature", "-created_at").values_list("id", flat=True)[:5]
    )
    project_detail_urls = [f"{base_project_details_url}?id={project_id}" for project_id in project_ids]
    while len(project_detail_urls) < 5:
        project_detail_urls.append(base_project_details_url)

    return render(
        request,
        "UI/home.html",
        {
            "wf_page": "698fb87304c94142e89f6592",
            "active_page": "home",
            "project_detail_urls": project_detail_urls,
            "projects_count": Project.objects.count(),
            "reviews_count": 6,
            "testimonials_count": 3,
            "images_count": ProjectImage.objects.count(),
        },
    )


def project(request):
    categories = ProjectCategory.objects.order_by("name")
    projects = Project.objects.prefetch_related("categories").order_by("-add_project_to_feature", "-created_at")

    return render(
        request,
        "UI/project.html",
        {
            "wf_page": "698fb87304c94142e89f661f",
            "active_page": "project",
            "categories": categories,
            "projects": projects.distinct(),
        },
    )


def about_us(request):
    return render(request, "UI/about-us.html", {"wf_page": "698fb87304c94142e89f661a", "active_page": "about-us"})


def contact_us(request):
    return render(request, "UI/contact-us.html", {"wf_page": "698fb87304c94142e89f65eb", "active_page": "contact-us"})


def gallery(request):
    categories = ProjectCategory.objects.order_by("name")
    images = ProjectImage.objects.select_related("project", "category").order_by("-id")

    return render(
        request,
        "UI/gallary.html",
        {
            "wf_page": "698fb87304c94142e89f3e5",
            "active_page": "gallery",
            "categories": categories,
            "images": images,
        },
    )


def project_details(request, project_id=None):
    project_id = project_id or request.GET.get("id")
    if project_id:
        project = get_object_or_404(Project, id=project_id)
    else:
        project = Project.objects.order_by("-add_project_to_feature", "-created_at").first()

    short_descriptions = []
    if project:
        short_descriptions = [
            text
            for text in [
                project.the_vision,
                project.the_brief,
                project.the_transformation,
                project.the_outcome,
            ]
            if text
        ]

    return render(
        request,
        "UI/project-details-dynamic.html",
        {
            "project": project,
            "short_descriptions": short_descriptions,
            "wf_page": "698fb87304c94142e89f6621",
            "active_page": "project",
        },
    )
