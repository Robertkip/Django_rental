import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['POST'])
def assignDeparmentPermision(request, id, module):
    if request.method == 'POST':
        # Extract the JSON data from the request
        request_data = request.data.get('request_data', {})
        permissions_str = request_data.get('permissions', '')

        # Clean up the permissions string to ensure valid JSON
        # Note: Adjust this logic based on actual issues you encounter
        permissions_str = permissions_str.replace('tickets', '"tickets"')  # Replace any known issues
        permissions_str = permissions_str.replace('ookings', '"bookings"')

        try:
            # Parse the JSON-formatted string into a Python list
            permissions = json.loads(permissions_str)
        except json.JSONDecodeError as e:
            return Response({"error": f"Invalid JSON format for permissions: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the data is in the expected format
        if not isinstance(permissions, list):
            return Response({"error": "Invalid data format. Expected a list of permissions."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Process the data (e.g., save to a model, etc.)
        # Here we're just returning the received data as a response
        return Response({"data": permissions, "id": id, "module": module}, status=status.HTTP_200_OK)
    
    return Response({"error": "Invalid request method. Use POST."}, status=status.HTTP_400_BAD_REQUEST)
