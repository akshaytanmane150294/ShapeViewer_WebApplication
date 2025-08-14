from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from .models import Prism
from .serializers import PrismSerializer
from django.shortcuts import get_object_or_404
from .utils import compute_surface_area_volume, get_cad_model_data

import os
import requests
import importlib

from django.conf import settings
from rest_framework.views import APIView

PLUGIN_DIR = os.path.join(settings.BASE_DIR, "plugins")


@api_view(['GET'])
def index(request):
    return Response({"message": "Welcome to Prism API!"})

@api_view(['GET'])
def list_prisms(request):
    prisms = Prism.objects.all()
    serializer = PrismSerializer(prisms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def prism_detail(request, id):
    if id.isdigit():
        prism = get_object_or_404(Prism, pk=int(id))
    else:
        prism = get_object_or_404(Prism, designation=id)

    serializer = PrismSerializer(prism)
    return Response(serializer.data)

@api_view(['GET'])
def compute_prism(request, id):
    if id.isdigit():
        prism = get_object_or_404(Prism, pk=int(id))
    else:
        prism = get_object_or_404(Prism, designation=id)

    prism_type = prism.prism_name.lower()

    try:
        # First, try using built-in function for known types
        if prism_type in ['rectangular', 'cylinder','cone']:  # Add more if you have
            result = compute_surface_area_volume(prism)
        else:
            # Fallback to plugin
            module_path = f"plugins.{prism_type}.compute_{prism_type}"
            compute_module = importlib.import_module(module_path)
            result = compute_module.compute(vars(prism))

        return Response(result)

    except ModuleNotFoundError:
        return Response({"error": f"No compute module found for prism type '{prism_type}'"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

@api_view(['GET'])
def prism_cad(request, id):
    try:
        prism = Prism.objects.get(designation=id)
    except Prism.DoesNotExist:
        return Response({"error": "Prism not found"}, status=404)

    prism_type = prism.prism_name.lower()

    try:
        if prism_type in ['rectangular', 'cylinder']:
            cad_data = get_cad_model_data(prism)
        else:
            module_path = f"plugins.{prism_type}.get_cad_model"
            cad_module = importlib.import_module(module_path)
            cad_data = cad_module.get_cad_model_data(prism)

        step_path = cad_data.get("step_file_path")

        if not step_path or not os.path.exists(step_path):
            return Response({"error": "STEP file not found"}, status=500)

        return FileResponse(open(step_path, 'rb'), content_type='application/step')

    except ModuleNotFoundError:
        return Response({"error": f"No CAD model module found for '{prism_type}'"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


class InstallPluginWithCADView(APIView):
    def post(self, request):
        github_urls = request.data.get("github_urls", [])
        
        if not github_urls or not isinstance(github_urls, list):
            return Response({"error": "A list of GitHub URLs is required."}, status=400)

        try:
            for url in github_urls:
                if "raw.githubusercontent.com" not in url:
                    return Response({"error": f"Invalid raw GitHub URL: {url}"}, status=400)

                # Get file name and prism name
                filename = url.split("/")[-1]

                if os.path.exists(prism_dir) and os.listdir(prism_dir):
                    return Response({"error": f"Plugin '{prism_name}' already exists."}, status=400)
                
                if not filename.endswith(".py"):
                    return Response({"error": f"Unsupported file type: {filename}"}, status=400)

                # Extract prism name from file like compute_cone.py → cone
                if filename.startswith("compute_") or filename == "get_cad_model.py":
                    prism_name = filename.replace("compute_", "").replace(".py", "") if filename.startswith("compute_") else url.split("/")[-2]
                else:
                    return Response({"error": f"Unexpected file: {filename}"}, status=400)

                # Create prism directory
                prism_dir = os.path.join(PLUGIN_ROOT, prism_name)
                os.makedirs(prism_dir, exist_ok=True)

                # Download and save file
                response = requests.get(url)
                if response.status_code != 200:
                    return Response({"error": f"Failed to download: {url}"}, status=400)

                file_path = os.path.join(prism_dir, filename)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(response.text)

            return Response({"status": "success", "message": "All plugin files installed successfully."})

        except Exception as e:
            return Response({"error": str(e)}, status=500)

