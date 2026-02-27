from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Project, ProjectCategory, ProjectImage


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
