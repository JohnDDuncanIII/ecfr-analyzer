import os
import re

# computes total wordcount from two of the largest agencies
# and dumps all of the truncated agency title subset(s) to a folder of the agency short_name
for agency in Agency.objects.filter(short_name__in=["TREAS", "EPA"]):
    cfr_refs = CFRReference.objects.filter(agency=agency)

    child_agencies = agency.children.all()

    for child in child_agencies:
        child_refs = CFRReference.objects.filter(agency=child)
        cfr_refs = cfr_refs | child_refs
    text_files_dir = os.path.join(settings.BASE_DIR, agency.short_name)
    os.makedirs(text_files_dir, exist_ok=True)

    for ref in cfr_refs:
        if ref.full_text:
            safe_title = re.sub(r"[^\w\s-]", "", str(ref))
            safe_agency = re.sub(r"[^\w\s-]", "", str(ref.agency))
            filename = f"{safe_title}_{safe_agency}.txt"
            filepath = os.path.join(text_files_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(ref.full_text)

        print(agency)
        for cfr_ref in cfr_refs:
            print(
                cfr_ref, f"{len(cfr_ref.full_text.split()): ,}", f"({cfr_ref.agency})"
            )
        print(
            agency,
            f"{sum(len(ref.full_text.split()) for ref in cfr_refs if ref.full_text): ,}",
            "\n",
        )

# these numbers differ from https://doge.gov/regulations
# Output:
# Department of Treasury
# Title 2 - Federal Financial Assistance, Chapter X  213 (Department of Treasury)
# Title 5 - Administrative Personnel, Chapter XXI  3,996 (Department of Treasury)
# Title 12 - Banks and Banking, Chapter I  716,041 (Comptroller of the Currency, Department of Treasury)
# Title 12 - Banks and Banking, Chapter XV  10,713 (Department of Treasury)
# Title 12 - Banks and Banking, Chapter XVI  4,336 (Office of Financial Research, Department of Treasury)
# Title 12 - Banks and Banking, Chapter XVIII  50,314 (Community Development Financial Institutions Fund, Department of Treasury)
# Title 17 - Commodity and Securities Exchanges, Chapter IV  38,578 (Department of Treasury)
# Title 26 - Internal Revenue, Chapter I  9,663,377 (Internal Revenue Service, Department of Treasury)
# Title 27 - Alcohol, Tobacco Products and Firearms, Chapter I  846,043 (Alcohol and Tobacco Tax and Trade Bureau, Department of Treasury)
# Title 31 - Money and Finance: Treasury, Subtitle A  265,014 (Office of Secretary of the Treasury, Department of Treasury)
# Title 31 - Money and Finance: Treasury, Chapter I  24,168 (Monetary Offices, Department of Treasury)
# Title 31 - Money and Finance: Treasury, Chapter II, Subchapter A  309,834 (Bureau of the Fiscal Service, Department of Treasury)
# Title 31 - Money and Finance: Treasury, Chapter II  309,843 (Fiscal Service, Department of Treasury)
# Title 31 - Money and Finance: Treasury, Chapter IX  10,844 (Department of Treasury)
# Title 31 - Money and Finance: Treasury, Chapter V  547,936 (Office of Foreign Assets Control, Department of Treasury)
# Title 31 - Money and Finance: Treasury, Chapter VI  1,637 (Bureau of Engraving and Printing, Department of Treasury)
# Title 31 - Money and Finance: Treasury, Chapter VIII  80,440 (Office of Investment Security, Department of Treasury)
# Title 31 - Money and Finance: Treasury, Chapter X  97,441 (Financial Crimes Enforcement Network, Department of Treasury)
# Title 48 - Federal Acquisition Regulations System, Chapter 10  8,744 (Department of Treasury)
# Department of Treasury  12,989,512

# Environmental Protection Agency
# Title 2 - Federal Financial Assistance, Chapter XV  8,706 (Environmental Protection Agency)
# Title 5 - Administrative Personnel, Chapter LIV  1,517 (Environmental Protection Agency)
# Title 40 - Protection of Environment, Chapter I  13,796,734 (Environmental Protection Agency)
# Title 40 - Protection of Environment, Chapter IV  2,358 (Environmental Protection Agency)
# Title 40 - Protection of Environment, Chapter VII  10,297 (Environmental Protection Agency)
# Title 41 - Public Contracts and Property Management, Chapter 115  466 (Environmental Protection Agency)
# Title 48 - Federal Acquisition Regulations System, Chapter 15  66,969 (Environmental Protection Agency)
# Environmental Protection Agency  13,887,047
