import os

from django.db import models

try:
    from PIL import Image, ImageOps
except ImportError:  # Pillow is optional in this environment.
    Image = None
    ImageOps = None


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Project Categories"

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    project_date = models.DateField(blank=True, null=True)
    listing_image = models.FileField(
        upload_to="projects/listing/",
        blank=True,
        help_text="Auto-cropped to 570x400 (57:40). Upload any high-quality image.",
    )
    main_image = models.FileField(
        upload_to="projects/main/",
        help_text="Auto-cropped to 1170x585 (2:1) for project-details hero.",
    )
    banner_image_one = models.FileField(
        upload_to="projects/banners/",
        blank=True,
        help_text="Auto-cropped to 1170x585 (2:1).",
    )
    banner_image_two = models.FileField(
        upload_to="projects/banners/",
        blank=True,
        help_text="Auto-cropped to 1170x585 (2:1).",
    )
    the_vision = models.TextField(blank=True, verbose_name="The Vision")
    the_brief = models.TextField(blank=True, verbose_name="The BrieF")
    the_transformation = models.TextField(blank=True, verbose_name="The Transformation")
    the_outcome = models.TextField(blank=True, verbose_name="The Outcome")
    google_map_iframe = models.TextField(
        blank=True,
        help_text="Paste full Google Maps iframe embed code.",
    )
    location_name = models.CharField(max_length=255, blank=True)
    location_city = models.CharField(max_length=120, blank=True)
    location_postcode = models.CharField(max_length=30, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    add_project_to_feature = models.BooleanField(default=False)
    categories = models.ManyToManyField(ProjectCategory, related_name="projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._process_image_field("listing_image", (570, 400))
        self._process_image_field("main_image", (1170, 585))
        self._process_image_field("banner_image_one", (1170, 585))
        self._process_image_field("banner_image_two", (1170, 585))

    def _process_image_field(self, field_name, target_size):
        if Image is None or ImageOps is None:
            return

        file_field = getattr(self, field_name, None)
        if not file_field:
            return

        if not hasattr(file_field, "path"):
            return

        try:
            with Image.open(file_field.path) as img:
                processed = ImageOps.fit(
                    img.convert("RGB"),
                    target_size,
                    method=Image.Resampling.LANCZOS,
                    centering=(0.5, 0.5),
                )
                ext = os.path.splitext(file_field.path)[1].lower()
                save_format = "PNG" if ext == ".png" else "JPEG"
                save_kwargs = {"optimize": True}
                if save_format == "JPEG":
                    save_kwargs["quality"] = 90
                processed.save(file_field.path, format=save_format, **save_kwargs)
        except OSError:
            return


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_images")
    image = models.FileField(
        upload_to="projects/gallery/",
        help_text="Auto-cropped to 1170x780 (3:2) for consistent gallery layout.",
    )
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        related_name="project_images",
        blank=True,
        null=True,
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.project.title} - Image {self.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._process_gallery_image()

    def _process_gallery_image(self):
        if Image is None or ImageOps is None:
            return

        file_field = self.image
        if not file_field or not hasattr(file_field, "path"):
            return

        try:
            with Image.open(file_field.path) as img:
                processed = ImageOps.fit(
                    img.convert("RGB"),
                    (1170, 780),  # 3:2 aspect ratio
                    method=Image.Resampling.LANCZOS,
                    centering=(0.5, 0.5),
                )
                ext = os.path.splitext(file_field.path)[1].lower()
                save_format = "PNG" if ext == ".png" else "JPEG"
                save_kwargs = {"optimize": True}
                if save_format == "JPEG":
                    save_kwargs["quality"] = 90
                processed.save(file_field.path, format=save_format, **save_kwargs)
        except OSError:
            return


class SiteSocialLinks(models.Model):
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site Social Links"
        verbose_name_plural = "Site Social Links"

    def __str__(self):
        return "Site Social Links"
