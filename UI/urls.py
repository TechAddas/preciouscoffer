from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home-page"),
    path("project", views.project, name="project"),
    path("about-us", views.about_us, name="about-us"),
    path("contact-us", views.contact_us, name="contact-us"),
    path("contact-us/", views.contact_us),
    path("gallery", views.gallery, name="gallery"),
    path("project-details", views.project_details, name="project-details"),
    path("project-details/<int:project_id>", views.project_details, name="project-details-by-id"),
    path(
        "testimonial/submit/<uuid:token>/",
        views.testimonial_public_submit,
        name="testimonial-public-submit",
    ),
    path("index.html", views.home, name="home-html"),
    path("project.html", views.project, name="project-html"),
    path("about-us.html", views.about_us, name="about-us-html"),
    path("contact-us.html", views.contact_us, name="contact-us-html"),
    path("gallary.html", views.gallery, name="gallery-html"),
    path("detail_projects.html", views.project_details, name="project-details-html"),
]
