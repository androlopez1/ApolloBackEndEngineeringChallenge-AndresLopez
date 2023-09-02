from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import viewsets, status
import xml.etree.ElementTree as ET
from .utils import xml_to_dict


class ConverterViewSet(viewsets.ViewSet):
    # Note this is not a restful API
    # We still use DRF to assess how well you know the framework
    parser_classes = [MultiPartParser]

    @action(methods=["POST"], detail=False, url_path="convert")
    def convert(self, request, **kwargs):
        uploaded_file = request.data.get('file')
        
        # Verify if file was uploaded correctly
        if not uploaded_file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            xml_content = uploaded_file.read().decode('utf-8')
            # Handling empty file error
            if not xml_content.strip():
                return Response({}, status=status.HTTP_200_OK)
            root = ET.fromstring(xml_content)
            serialized_data = xml_to_dict(root)
            return Response(serialized_data, status=status.HTTP_200_OK, content_type='application/json')
        except ET.ParseError:
            return Response({'error': 'XML File not valid'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

