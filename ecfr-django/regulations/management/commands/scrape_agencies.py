import requests
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from regulations.models import Agency, CFRReference, Title

BASE_URL = "https://www.ecfr.gov/api"


class Command(BaseCommand):
    help = "Import agencies data from eCFR API"

    def handle(self, *args, **options):
        # First process titles
        self.process_titles()

        # Then process agencies
        response = requests.get(f"{BASE_URL}/admin/v1/agencies.json")
        data = response.json()
        self.process_agencies(data["agencies"])

        self.stdout.write(
            self.style.SUCCESS("Successfully imported agencies and titles data")
        )

    def process_titles(self):
        response = requests.get(f"{BASE_URL}/versioner/v1/titles.json")
        data = response.json()

        titles_to_create = []
        for title_data in data["titles"]:
            title = Title(
                number=title_data["number"],
                name=title_data["name"],
                latest_amended_on=parse_date(title_data["latest_amended_on"])
                if title_data["latest_amended_on"]
                else None,
                latest_issue_date=parse_date(title_data["latest_issue_date"])
                if title_data["latest_issue_date"]
                else None,
                up_to_date_as_of=parse_date(title_data["up_to_date_as_of"])
                if title_data["up_to_date_as_of"]
                else None,
                reserved=title_data["reserved"],
            )
            titles_to_create.append(title)

        Title.objects.bulk_create(
            titles_to_create,
            ignore_conflicts=True,
        )

    def process_agencies(self, agencies, parent=None):
        title_lookup = {title.number: title for title in Title.objects.all()}

        # Lists to collect objects for bulk creation
        agencies_to_create = []

        for agency_data in agencies:
            # Create agency instance without saving
            agency = Agency(
                slug=agency_data["slug"],
                name=agency_data["name"],
                short_name=agency_data["short_name"] or "",
                display_name=agency_data["display_name"],
                sortable_name=agency_data["sortable_name"],
                parent=parent,
            )
            agencies_to_create.append(agency)

        # Bulk create agencies and get the created instances
        created_agencies = Agency.objects.bulk_create(
            agencies_to_create,
            ignore_conflicts=True,
        )

        # constant query
        agency_lookup = {
            agency.slug: agency
            for agency in Agency.objects.filter(
                slug__in=[agency.slug for agency in created_agencies]
            )
        }

        # Now create CFR references for the saved agencies
        cfr_refs_to_create = []
        for agency_data, agency in zip(agencies, created_agencies):
            # linear queries
            # actual_agency = Agency.objects.get(slug=agency.slug)
            # constant query
            actual_agency = agency_lookup[agency.slug]

            # Collect CFR references
            for ref in agency_data["cfr_references"]:
                title_number = int(ref["title"])
                cfr_ref = CFRReference(
                    agency=actual_agency,
                    title=title_lookup[title_number],
                    chapter=ref.get("chapter", ""),
                    subtitle=ref.get("subtitle", ""),
                    part=ref.get("part", ""),
                    subchapter=ref.get("subchapter", ""),
                )
                cfr_refs_to_create.append(cfr_ref)

        # Bulk create CFR references
        if cfr_refs_to_create:
            CFRReference.objects.bulk_create(
                cfr_refs_to_create,
                ignore_conflicts=True,
            )

        # Process child agencies recursively
        for agency_data, agency in zip(agencies, created_agencies):
            if agency_data.get("children"):
                actual_agency = agency_lookup[agency.slug]
                self.process_agencies(
                    agency_data["children"],
                    parent=actual_agency,
                )
