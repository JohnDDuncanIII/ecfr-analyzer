from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Agency, Title
from .serializers import AgencyWordCountSerializer, TitleSerializer


class AgencyResource(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AgencyWordCountSerializer

    def get_queryset(self):
        return Agency.objects.order_by("-cfr_word_count").distinct("cfr_word_count")

    @action(detail=True, methods=["get"], url_path="references")
    def get_references(self, request, pk=None):
        try:
            agency = Agency.objects.get(slug=pk)
            # Get direct references
            references = agency.cfr_references.all()

            # Get references from all child agencies
            for child in agency.children.all():
                references |= child.cfr_references.all()
                # Get references from grandchildren
                for grandchild in child.children.all():
                    references |= grandchild.cfr_references.all()
            data = {
                "agency_word_count": agency.cfr_word_count,
                "references": [
                    {
                        "title": f"{ref.title.name} {ref.title.number}"
                        if ref.title
                        else None,
                        "subtitle": ref.subtitle,
                        "chapter": ref.chapter,
                        "subchapter": ref.subchapter,
                        "part": ref.part,
                        "subpart": ref.subpart,
                        "section": ref.section,
                        "full_text": ref.full_text,
                    }
                    for ref in references
                ],
            }
            return Response(data)
        except Agency.DoesNotExist:
            return Response({"error": "Agency not found"}, status=404)


class AgencyNameResource(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AgencyWordCountSerializer

    def get_queryset(self):
        return Agency.objects.order_by("name")


class TitleResource(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TitleSerializer

    def get_queryset(self):
        return Title.objects.all()
