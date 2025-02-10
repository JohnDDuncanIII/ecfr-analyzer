from django.db import models


class Agency(models.Model):
    """
    Represents a federal agency or sub-agency with CFR references
    """

    name = models.CharField(max_length=255)
    # bug in API: Agency w/ short_name "Military Compensation and Retirement Modernization Commission"
    short_name = models.CharField(max_length=63, blank=True, null=True)
    display_name = models.CharField(max_length=255)
    sortable_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    cfr_word_count = models.BigIntegerField(
        null=True,
        blank=True,
        default=0,
        help_text="Total word count of all related CFR reference full texts",
    )

    # Self-referential relationship for parent/child agencies
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    class Meta:
        verbose_name_plural = "agencies"
        ordering = ["sortable_name"]

    def __str__(self):
        return self.display_name


class CFRReferenceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().defer("full_text")


class CFRReference(models.Model):
    """
    Represents a Code of Federal Regulations (CFR) reference for an Agency
    """

    objects = CFRReferenceManager()

    # foreign keys
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name="cfr_references",
    )

    # metadata
    title = models.ForeignKey(
        "Title",
        on_delete=models.CASCADE,
        related_name="cfr_references",
    )
    subtitle = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )
    chapter = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )
    subchapter = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )
    part = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )
    subpart = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )
    section = models.CharField(
        max_length=20,
        blank=True,
    )

    # text to be processed for word count
    full_text = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(null=True)

    class Meta:
        unique_together = [
            "agency",
            "title",
            "chapter",
            "subtitle",
            "part",
            "subchapter",
        ]
        ordering = ["title", "chapter"]

    def __str__(self):
        parts = [f"Title {self.title}"]
        if self.subtitle:
            parts.append(f"Subtitle {self.subtitle}")
        if self.chapter:
            parts.append(f"Chapter {self.chapter}")
        if self.subchapter:
            parts.append(f"Subchapter {self.subchapter}")
        if self.part:
            parts.append(f"Part {self.part}")
        return ", ".join(parts)


class Title(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    latest_amended_on = models.DateField(null=True, blank=True)
    latest_issue_date = models.DateField(null=True, blank=True)
    up_to_date_as_of = models.DateField(null=True, blank=True)
    reserved = models.BooleanField(default=False)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"{self.number} - {self.name}"
