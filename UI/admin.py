from django.contrib import admin, messages
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    Project,
    ProjectCategory,
    ProjectImage,
    SiteSocialLinks,
    Testimonial,
    TestimonialInvite,
)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "thumbnail_preview", "category", "sort_order")
    readonly_fields = ("thumbnail_preview",)

    def thumbnail_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="height: 70px; width: auto; border-radius: 4px;" />',
                obj.image.url,
            )
        return "No image"

    thumbnail_preview.short_description = "Preview"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "add_project_to_feature", "created_at")
    list_filter = ("add_project_to_feature", "categories")
    search_fields = ("title", "the_vision", "the_brief", "the_transformation", "the_outcome")
    filter_horizontal = ("categories",)
    inlines = [ProjectImageInline]
    readonly_fields = (
        "listing_image_preview",
        "main_image_preview",
        "banner_image_one_preview",
        "banner_image_two_preview",
        "map_picker",
    )
    fieldsets = (
        ("Project Information", {"fields": ("title", "project_date")}),
        (
            "Listing Image",
            {
                "description": "Auto-cropped to 57:40 and saved as 570x400.",
                "fields": ("listing_image", "listing_image_preview"),
            },
        ),
        (
            "Main Image",
            {
                "description": "Auto-cropped to 1170x585 (2:1) for details page hero.",
                "fields": ("main_image", "main_image_preview"),
            },
        ),
        (
            "Short Descriptions",
            {
                "description": "Project narrative sections shown on project details page.",
                "fields": (
                    "the_vision",
                    "the_brief",
                    "the_transformation",
                    "the_outcome",
                ),
            },
        ),
        (
            "Banner Images",
            {
                "description": "Auto-cropped to 1170x585 (2:1) for both banners.",
                "fields": (
                    "banner_image_one",
                    "banner_image_one_preview",
                    "banner_image_two",
                    "banner_image_two_preview",
                ),
            },
        ),
        (
            "Location",
            {
                "description": "Pick point on map to auto-fill postcode and coordinates, or type city manually.",
                "fields": ("location_city", "location_postcode", "location_name", "latitude", "longitude", "map_picker"),
            },
        ),
        ("Google Map (Optional Override)", {"fields": ("google_map_iframe",)}),
        ("Services (Categories)", {"fields": ("categories",)}),
        ("Feature", {"fields": ("add_project_to_feature",)}),
    )

    class Media:
        css = {
            "all": ("https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",),
        }
        js = (
            "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
            "js/admin-project-map.js",
        )

    def listing_image_preview(self, obj):
        if obj and obj.listing_image:
            return format_html(
                '<img src="{}" style="max-width: 180px; height: auto; border-radius: 6px;" />',
                obj.listing_image.url,
            )
        return "No image"

    listing_image_preview.short_description = "Listing Image Preview"

    def main_image_preview(self, obj):
        if obj and obj.main_image:
            return format_html(
                '<img src="{}" style="max-width: 260px; height: auto; border-radius: 6px;" />',
                obj.main_image.url,
            )
        return "No image"

    main_image_preview.short_description = "Main Image Preview"

    def banner_image_one_preview(self, obj):
        if obj and obj.banner_image_one:
            return format_html(
                '<img src="{}" style="max-width: 260px; height: auto; border-radius: 6px;" />',
                obj.banner_image_one.url,
            )
        return "No image"

    banner_image_one_preview.short_description = "Banner 1 Preview"

    def banner_image_two_preview(self, obj):
        if obj and obj.banner_image_two:
            return format_html(
                '<img src="{}" style="max-width: 260px; height: auto; border-radius: 6px;" />',
                obj.banner_image_two.url,
            )
        return "No image"

    banner_image_two_preview.short_description = "Banner 2 Preview"

    def map_picker(self, obj):
        return mark_safe(
            """
            <div style="margin: 10px 0 8px 0; display:flex; gap:8px; flex-wrap:wrap;">
              <input
                type="text"
                id="project-map-search"
                placeholder="Search place, city, or address"
                style="min-width:300px; padding:6px 10px;"
              />
              <button type="button" class="button" id="project-map-search-btn">Search</button>
            </div>
            <div
              id="project-map-picker"
              style="height:360px; max-width:900px; border:1px solid #d9d9d9; border-radius:6px;"
            ></div>
            <p style="margin-top:8px; color:#666;">
              Click map to set coordinates. Search/click also tries to fill postcode.
            </p>
            """
        )

    map_picker.short_description = "Map Picker"


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "thumbnail_preview", "sort_order")
    list_filter = ("category", "project")
    search_fields = ("project__title",)
    readonly_fields = ("thumbnail_preview",)

    def thumbnail_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="height: 70px; width: auto; border-radius: 4px;" />',
                obj.image.url,
            )
        return "No image"

    thumbnail_preview.short_description = "Preview"


@admin.register(SiteSocialLinks)
class SiteSocialLinksAdmin(admin.ModelAdmin):
    list_display = ("id", "instagram_url", "facebook_url", "twitter_url", "linkedin_url")
    fieldsets = (
        (
            "Social Media Links",
            {
                "fields": ("instagram_url", "facebook_url", "twitter_url", "linkedin_url"),
                "description": "Add full links used across the UI footer and social sections.",
            },
        ),
    )

    def has_add_permission(self, request):
        if SiteSocialLinks.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "role", "quote")


@admin.register(TestimonialInvite)
class TestimonialInviteAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at", "expires_at", "is_used", "is_expired_display", "sent_at")
    list_filter = ("is_used",)
    search_fields = ("email",)
    readonly_fields = ("token", "public_link_preview", "created_at", "sent_at")
    actions = ("send_invite_email",)
    fieldsets = (
        (
            "Invite Details",
            {
                "fields": ("email", "token", "expires_at", "is_used", "public_link_preview"),
                "description": "Create and share a public testimonial submission link. Default expiry is 10 days.",
            },
        ),
        ("Tracking", {"fields": ("created_at", "sent_at")}),
    )

    def is_expired_display(self, obj):
        return obj.is_expired

    is_expired_display.boolean = True
    is_expired_display.short_description = "Expired"

    def public_link_preview(self, obj):
        if not obj.pk:
            return "Save first to generate link."
        path = reverse("testimonial-public-submit", kwargs={"token": str(obj.token)})
        return format_html('<a href="{0}" target="_blank">{0}</a>', path)

    public_link_preview.short_description = "Public Link"

    @admin.action(description="Send testimonial invite email")
    def send_invite_email(self, request, queryset):
        sent_count = 0
        skipped = 0
        failure_reasons = []
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")

        for invite in queryset:
            if invite.is_used or invite.is_expired:
                skipped += 1
                continue

            invite_url = request.build_absolute_uri(
                reverse("testimonial-public-submit", kwargs={"token": str(invite.token)})
            )
            subject = "Share your testimonial - Precious Coffer"
            message = (
                "Hi,\n\n"
                "We would love your feedback. Please use the link below to submit your testimonial:\n"
                f"{invite_url}\n\n"
                "This link expires in 10 days.\n\n"
                "Thank you,\n"
                "Precious Coffer Team"
            )

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[invite.email],
                    fail_silently=False,
                )
                invite.sent_at = timezone.now()
                invite.save(update_fields=["sent_at"])
                sent_count += 1
            except Exception as exc:
                skipped += 1
                failure_reasons.append(f"{invite.email}: {exc}")

        if sent_count:
            self.message_user(request, f"Sent {sent_count} invite email(s).")
        if skipped:
            self.message_user(
                request,
                f"Skipped {skipped} invite(s) because they are expired/used or email sending failed.",
                level=messages.WARNING,
            )
        if failure_reasons:
            self.message_user(
                request,
                "Failures: " + "; ".join(failure_reasons[:5]),
                level=messages.ERROR,
            )
