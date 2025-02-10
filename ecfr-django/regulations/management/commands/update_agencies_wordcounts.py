from django.core.management.base import BaseCommand
from regulations.models import Agency, CFRReference

BASE_URL = "https://www.ecfr.gov/api"


class Command(BaseCommand):
    help = "Update agency word_count from associated CFRReference full_text data scraped from eCFR API"

    def handle(self, *args, **options):
        # For each agency, calculate total word count of related CFR references
        for agency in Agency.objects.all():
            # Get all related CFR references for this agency and its children
            cfr_refs = CFRReference.objects.filter(agency=agency)

            # Get all child agencies
            child_agencies = agency.children.all()

            # Add CFR references from child agencies
            for child in child_agencies:
                child_refs = CFRReference.objects.filter(agency=child)
                cfr_refs = cfr_refs | child_refs

            # Calculate word count by counting spaces + 1
            total_words = sum(
                len(ref.full_text.split()) for ref in cfr_refs if ref.full_text
            )

            print(f"{agency}: {total_words} words")

            print(total_words)
            agency.cfr_word_count = total_words
            agency.save()

        self.stdout.write(
            self.style.SUCCESS("Successfully updated word_count for agencies!")
        )
