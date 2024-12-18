# from django.utils.deprecation import MiddlewareMixin
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import InvalidToken
# from django.http import JsonResponse

# class TokenValidationMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         excluded_paths = ['/api/login/', '/api/register/']
#         print(f"Request path: {request.path}")

#         if request.path in excluded_paths:
#             print("Skipping token validation for this path.")
#             return None

#         auth_header = request.headers.get('Authorization')
#         if not auth_header or not auth_header.startswith('Bearer '):
#             print("No Authorization header found.")
#             request.user = None
#             return JsonResponse({"error": "Authentication credentials were not provided."}, status=401)

#         token = auth_header.split(' ')[1]
#         print(f"Token: {token}")

#         try:
#             jwt_auth = JWTAuthentication()
#             validated_token = jwt_auth.get_validated_token(token)
#             user = jwt_auth.get_user(validated_token)
#             request.user = user
#             print(f"Authenticated user: {user.username}")
#         except InvalidToken:
#             print("Invalid token.")
#             request.user = None
#             return JsonResponse({"error": "Invalid or expired token."}, status=401)

