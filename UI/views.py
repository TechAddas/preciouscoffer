from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Project, ProjectCategory, ProjectImage, Testimonial, TestimonialInvite


def _fallback_testimonials():
    return [
        {
            "name": "Ronald Richards",
            "role": "CEO, Anderson Real Estate",
            "quote": "Working with this architectural agency was a game-changer for our commercial projects. Their innovative designs and attention to detail exceeded our expectations, delivering a final product that perfectly aligned with our brand and vision.",
        },
        {
            "name": "Sarah Bennett",
            "role": "Homeowner",
            "quote": "The renovation of our home was seamless, thanks to the team’s expertise and commitment to quality. They truly listened to our needs and transformed our outdated space into a modern, functional, and beautiful home.",
        },
        {
            "name": "David Foster",
            "role": "Director of Operations",
            "quote": "Their ability to blend sustainable practices with cutting-edge design is unparalleled. We were thrilled with the results and impressed by their dedication to creating environmentally-friendly and aesthetically pleasing spaces.",
        },
        {
            "name": "James Miller",
            "role": "Property Developer",
            "quote": "Collaborating with this team was an absolute pleasure. Their creative approach and professionalism made the process smooth, and the final designs were nothing short of stunning.",
        },
        {
            "name": "Emily Carter",
            "role": "Interior Designer",
            "quote": "This team brought a fresh perspective to our development projects. Their innovative ideas and thorough project management ensured everything was delivered on time and within budget.",
        },
        {
            "name": "Noah Wilson",
            "role": "Client",
            "quote": "Build quality was consistent and the team handled details carefully. We would confidently recommend them for residential and refurbishment work.",
        },
    ]


def _home_testimonials_data():
    testimonials_qs = Testimonial.objects.all()
    if testimonials_qs.exists():
        return list(testimonials_qs.values("name", "role", "quote"))
    return _fallback_testimonials()


def home(request):
    base_project_details_url = reverse("project-details")
    project_ids = list(
        Project.objects.order_by("-add_project_to_feature", "-created_at").values_list("id", flat=True)[:5]
    )
    project_detail_urls = [f"{base_project_details_url}?id={project_id}" for project_id in project_ids]
    while len(project_detail_urls) < 5:
        project_detail_urls.append(base_project_details_url)

    home_testimonials = _home_testimonials_data()

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
            "home_testimonials": home_testimonials,
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
    testimonials_qs = Testimonial.objects.all()
    if testimonials_qs.exists():
        testimonials = testimonials_qs
    else:
        testimonials = _fallback_testimonials()
    return render(
        request,
        "UI/about-us.html",
        {
            "wf_page": "698fb87304c94142e89f661a",
            "active_page": "about-us",
            "testimonials": testimonials,
            "projects_count": Project.objects.count(),
            "reviews_count": 6,
            "testimonials_count": 3,
            "images_count": ProjectImage.objects.count(),
        },
    )


def contact_us(request):
    testimonials_qs = Testimonial.objects.all()
    if testimonials_qs.exists():
        testimonials = testimonials_qs
    else:
        testimonials = _fallback_testimonials()

    context = {
        "wf_page": "698fb87304c94142e89f65eb",
        "active_page": "contact-us",
        "form_data": {},
        "form_success": False,
        "form_error": "",
        "testimonials": testimonials,
    }

    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        message_text = (request.POST.get("field") or "").strip()

        context["form_data"] = {"name": name, "email": email, "field": message_text}

        if not name or not email or not message_text:
            context["form_error"] = "Please fill all fields before submitting."
        else:
            recipient = getattr(settings, "CONTACT_RECEIVER_EMAIL", None) or getattr(
                settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"
            )
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")
            subject = f"Contact Form Submission - {name}"
            body = (
                f"Name: {name}\n"
                f"Email: {email}\n\n"
                f"Message:\n{message_text}\n"
            )

            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=from_email,
                    recipient_list=[recipient],
                    fail_silently=False,
                )
                ack_subject = "We received your message - Precious Coffer"
                ack_body = (
                    f"Hi {name},\n\n"
                    "Thank you for contacting Precious Coffer. "
                    "We have received your message and will get back to you shortly.\n\n"
                    "Regards,\n"
                    "Precious Coffer Team"
                )
                try:
                    send_mail(
                        subject=ack_subject,
                        message=ack_body,
                        from_email=from_email,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                except Exception:
                    # Do not block successful form submission if acknowledgement fails.
                    pass
                context["form_success"] = True
                context["form_data"] = {}
            except Exception:
                context["form_error"] = "Message could not be sent right now. Please try again."

    return render(request, "UI/contact-us.html", context)


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


def testimonial_public_submit(request, token):
    invite = get_object_or_404(TestimonialInvite, token=token)
    is_invalid = invite.is_used or invite.is_expired

    context = {
        "invite": invite,
        "is_invalid": is_invalid,
        "submitted": False,
        "form_error": "",
        "form_data": {},
        "wf_page": "698fb87304c94142e89f65eb",
        "active_page": "",
    }

    if request.method == "POST" and not is_invalid:
        name = (request.POST.get("name") or "").strip()
        role = (request.POST.get("role") or "").strip()
        quote = (request.POST.get("quote") or "").strip()
        photo = request.FILES.get("photo")

        context["form_data"] = {"name": name, "role": role, "quote": quote}

        if not name or not quote:
            context["form_error"] = "Name and testimonial are required."
        else:
            Testimonial.objects.create(
                name=name,
                role=role,
                quote=quote,
                photo=photo,
                is_active=True,
            )
            invite.is_used = True
            invite.save(update_fields=["is_used"])
            context["submitted"] = True

    return render(request, "UI/testimonial-submit.html", context)
