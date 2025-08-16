import tempfile,subprocess,shutil  
import os
import requests
import importlib
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from .models import Prism
from .serializers import PrismSerializer
from django.shortcuts import get_object_or_404
from .utils import compute_surface_area_volume, get_cad_model_data


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
            result = compute_module.compute_surface_area_volume(prism)

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
        if prism_type in ['rectangular', 'cylinder','cone']:
            cad_data = get_cad_model_data(prism)
        else:
            module_path = f"plugins.{prism_type}.get_cad_model_data"
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


@api_view(['POST'])
def install_plugin(request):
    github_urls = request.data.get("github_urls", [])
    if not github_urls or not isinstance(github_urls, list):
        return Response({"error": "A list of GitHub URLs is required."}, status=400)

    try:
        for url in github_urls:
            if not url.endswith(".git"):
                return Response({"error": f"Invalid GitHub repo URL: {url}"}, status=400)

            temp_dir = tempfile.mkdtemp()
            try:
                # Clone repo
                subprocess.check_call(["git", "clone", url, temp_dir])

                found_compute = None
                found_cad = None
                prism_name = None

                # Search for compute_xxx.py and get_cad_model_data.py
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.startswith("compute_") and file.endswith(".py"):
                            found_compute = os.path.join(root, file)
                            prism_name = file.replace("compute_", "").replace(".py", "")
                        elif file == "get_cad_model_data.py":
                            found_cad = os.path.join(root, file)

                if not found_compute or not found_cad or not prism_name:
                    return Response({"error": f"Required plugin files not found in {url}"}, status=400)

                # Make prism folder
                prism_dir = os.path.join(PLUGIN_DIR, prism_name)
                os.makedirs(prism_dir, exist_ok=True)

                # Copy both files to same folder
                shutil.copy(found_compute, prism_dir)
                shutil.copy(found_cad, prism_dir)

            finally:
                shutil.rmtree(temp_dir)

        return Response({"status": "success", "message": "Plugins installed successfully."})

    except subprocess.CalledProcessError as e:
        return Response({"error": f"Git clone failed: {str(e)}"}, status=500)
    except Exception as e:
        return Response({"error": str(e)}, status=500)



