import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

# ecfr
from regulations.models import CFRReference


class Command(BaseCommand):
    help = "Fetches full text for CFR references"

    def get_latest_date(self):
        url = "https://www.ecfr.gov/api/versioner/v1/titles"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Get all unique up_to_date_as_of values, excluding None
            dates = {
                title["up_to_date_as_of"]
                for title in data["titles"]
                if title["up_to_date_as_of"]
            }

            if not dates:
                self.stdout.write(self.style.ERROR("No valid dates found"))
                return

            # Convert to datetime objects for comparison
            date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

            # Get the most recent date and convert back to string
            latest_date = max(date_objects).strftime("%Y-%m-%d")

            self.stdout.write(self.style.SUCCESS(latest_date))
            return latest_date
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching data: {str(e)}"))
        except (KeyError, ValueError) as e:
            self.stdout.write(self.style.ERROR(f"Error parsing data: {str(e)}"))

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            type=str,
            help="Date in YYYY-MM-DD format",
            default=self.get_latest_date(),
        )
        parser.add_argument(
            "--include-headers",
            action="store_true",
            help="Include headers in the text output",
            default=False,
        )
        parser.add_argument(
            "--title", type=int, help="Specific title number to process"
        )

    def build_url(self, base_url, ref):
        """Builds URL with appropriate query parameters based on CFRReference"""
        params = []

        if ref.subtitle:
            params.append(f"subtitle={ref.subtitle}")
        if ref.chapter:
            params.append(f"chapter={ref.chapter}")
        if ref.subchapter:
            params.append(f"subchapter={ref.subchapter}")
        if ref.part:
            params.append(f"part={ref.part}")
        if ref.subpart:
            params.append(f"subpart={ref.subpart}")
        if ref.section:
            params.append(f"section={ref.section}")

        query_string = "&".join(params)
        return f"{base_url}/title-{ref.title.number}.xml{f'?{query_string}' if query_string else ''}"

    def extract_text(self, xml_root, ref, include_headers=True):
        """
        Extracts text content from XML at the most specific/lowest division specified in the reference.

        Args:
            xml_root: XML root element
            ref: CFRReference object containing title, chapter, subchapter, etc.
            include_headers: Whether to include section headers
        """

        # Define hierarchy from highest to lowest
        # https://github.com/usgpo/bulk-data/blob/main/ECFR-XML-User-Guide.md
        hierarchy = [
            (
                "DIV1",
                "TITLE",
                "title_id",
                lambda x: str(x.number),
            ),  # title is a foreign key
            ("DIV2", "SUBTITLE", "subtitle", str),
            ("DIV3", "CHAPTER", "chapter", str),
            ("DIV4", "SUBCHAP", "subchapter", str),
            ("DIV5", "PART", "part", str),
            ("DIV6", "SUBPART", "subpart", str),
            ("DIV8", "SECTION", "section", str),
        ]

        # Find the lowest specified division in our reference
        target_level = None
        target_value = None

        for div_tag, div_type, ref_attr, converter in reversed(hierarchy):
            ref_value = getattr(ref, ref_attr)
            if ref_value:
                target_level = (div_tag, div_type)
                target_value = converter(ref_value)
                break

        if not target_level:
            return ""

        text_parts = []
        in_target_division = False

        for elem in xml_root.iter():
            # Check if we're entering our target division
            if (
                elem.tag == target_level[0]
                and elem.get("TYPE") == target_level[1]
                and elem.get("N")
                and elem.get("N").strip() == target_value.strip()
            ):
                in_target_division = True

                # Add division header if requested
                if include_headers and elem.find("HEAD") is not None:
                    head_text = elem.find("HEAD").text.strip()
                    if target_level[1] == "SECTION":
                        text_parts.append(f"\n§ {elem.get('N')} {head_text}\n")
                    else:
                        text_parts.append(
                            f"\n{target_level[1]} {elem.get('N')}—{head_text}\n"
                        )

                continue

            # Check if we're exiting our target division (by finding next division of same type)
            if (
                in_target_division
                and elem.tag == target_level[0]
                and elem.get("TYPE") == target_level[1]
            ):
                break

            # Process content within our target division
            if in_target_division:
                if elem.tag == "P":
                    text = "".join(elem.itertext()).strip()
                    if text:
                        text_parts.append(text + "\n")

                elif elem.tag == "AUTH":
                    pspace = elem.find("PSPACE")
                    if elem.find("PSPACE") is not None and pspace.text:
                        text_parts.append(
                            "\nAuthority: " + elem.find("PSPACE").text.strip() + "\n"
                        )

                elif elem.tag == "SOURCE":
                    pspace = elem.find("PSPACE")
                    if elem.find("PSPACE") is not None and pspace.text:
                        text_parts.append(
                            "\nSource: " + elem.find("PSPACE").text.strip() + "\n"
                        )

        return "".join(text_parts).strip()

    def handle(self, *args, **options):
        date = options["date"]
        base_url = f"https://www.ecfr.gov/api/versioner/v1/full/{date}"

        # Get queryset of references
        references = CFRReference.objects.all()
        if options["title"]:
            references.filter(title__number=options["title"])

        xml_cache = None

        for ref in references.order_by("title__number", "chapter", "section"):
            try:
                url = self.build_url(base_url, ref)
                self.stdout.write(f"Fetching: {url}")

                response = requests.get(url)
                response.raise_for_status()

                xml_cache = ET.fromstring(response.content)

                text = self.extract_text(
                    xml_cache,
                    ref,
                    options["include_headers"],
                )
                print(text)
                if text:
                    with transaction.atomic():
                        ref.full_text = text
                        ref.last_updated = timezone.now()
                        ref.save()
                        self.stdout.write(self.style.SUCCESS(f"Updated text for {ref}"))
                else:
                    self.stdout.write(self.style.WARNING(f"No text found for {ref}"))

            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Error fetching {ref}: {str(e)}"))
            except ET.ParseError as e:
                self.stdout.write(
                    self.style.ERROR(f"Error parsing XML for {ref}: {str(e)}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Unexpected error processing {ref}: {str(e)}")
                )
