import os
import json
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET'])
def read_json(
request):
    if request.method == 'GET':
        # Specify the directory containing your JSON files
        json_dir = os.path.join(os.getcwd(), 'permissions', 'modules')

        # List all JSON files in the directory and remove the .json extension
        json_files = [os.path.splitext(f)[0] for f in os.listdir(json_dir) if f.endswith('.json')]
        
        # Return the list of JSON filenames without the extension in the response
        return Response({"modules": json_files})
    


def extract_permissions(children_dict, parent_key=""):
    permissions = []
    for key, value in children_dict.items():
        current_key = f"{parent_key}.{key}" if parent_key else key
        permissions.append(current_key)
        if "children" in value:
            permissions.extend(extract_permissions(value["children"], current_key))
    return permissions

@api_view(['GET'])
def single_json(request, module):
    if request.method == 'GET':
        # Specify the directory containing your JSON files
        json_dir = os.path.join(os.getcwd(), 'permissions', 'modules')
        
        # Build the full path to the JSON file with the provided module name
        json_path = os.path.join(json_dir, f"{module}.json")
        
        # Check if the file exists
        if os.path.exists(json_path):
            # Read the JSON file
            with open(json_path, 'r') as json_file:
                json_content = json.load(json_file)
            
            # Extract the permissions
            children = json_content.get('children', {})
            permissions = extract_permissions(children)
            
            # Prepare the response
            response = {
                "module": json_content.get("main", module),
                "permissions": permissions
            }
            
            # Return the response
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import DepartmentPermission  # Import your model
@api_view(['POST'])
def savePermisions(request, id, module):
    # Extract the body of the request
    request_body = request.data
    permissions_str = request.data.get('permission', '[]') 
    # Prepare the response with the parameters from the URL and request body
    response_data = {
        'department_id': id,
        'department_module': module,
        'request_body': request_body
    }

    department_permission = DepartmentPermission(
            permissions=permissions_str,  # Store permissions as a string
            department_id_id=id,
            module=module,
            urls='urls'
        )
        
        # Save to the database
    department_permission.save()
    
    return Response(response_data, status=status.HTTP_200_OK)