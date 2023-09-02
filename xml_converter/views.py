import json
import xml.etree.ElementTree as ET
from django.http import JsonResponse
from django.shortcuts import render
from .utils import xml_to_dict

from .forms import UploadFileForm


def upload_page(request):
    if request.method == 'POST':
        response_data = {}
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            xml_content = form.cleaned_data['file'].read()
            
            # Handling empty file error
            if not xml_content.strip():
                return JsonResponse(response_data, json_dumps_params={'indent': 4})
            
            try:
                root = ET.fromstring(xml_content)
                # Converts root element into a dict
                serialized_data = xml_to_dict(root)
                
                response_data.update(serialized_data)
            except ET.ParseError:
                response_data['error'] = "XML file not valid"

            return JsonResponse(response_data, json_dumps_params={'indent': 4})

    else:
        form = UploadFileForm()

    return render(request, 'upload_page.html', {'form': form})


    
