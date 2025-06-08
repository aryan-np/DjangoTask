from rest_framework.response import Response
from .serializers import TodoModelSerializer,LoginSerializer,RegisterSerializer
from .models import TodoModel
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.pagination import PageNumberPagination

from rest_framework.authtoken.models import Token

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAndCreateTodo(request):
    
    # Handle GET request - return all todo items of user
    if request.method=='GET':
         # retrieving all list of the user and serializing into json
        lists = TodoModel.objects.filter(owner=request.user).order_by('id')
        
        # check if completed parameter exists
        completedParam = request.query_params.get('completed')
        
        # apply filter to completed (true or false)
        if completedParam is not None:
            if completedParam.lower() == 'true':
                lists = lists.filter(completed=True)
            elif completedParam.lower() == 'false':
                lists = lists.filter(completed=False)
            
        
        # returning list of 2 todos in 1 page
        paginator = PageNumberPagination()
        paginator.page_size=2
        
        result_set = paginator.paginate_queryset(lists,request)
        
        serializer = TodoModelSerializer(result_set,many=True)
        return paginator.get_paginated_response(serializer.data)
    
    
    # Handle POST request create new todo item
    if request.method=='POST':
        # retrieve title and description from req body
        title = request.data.get('title')
        description = request.data.get('description')
        owner = request.user
        if not title or not description:
            return Response({'error': 'Both title and description are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        #serializing the data and saving it  
        serializer = TodoModelSerializer(data={"title":title,"description":description})
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','PUT','PATCH','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUpdateOrDeleteTodo(request, id):
    # retrieced id from path parameter
    if not id:
        return Response({"error":"Missing todo id"},status=status.HTTP_404_NOT_FOUND)
    
    # checking if todo with retrieved exists
    try:
        todo = TodoModel.objects.get(id=id)
    except TodoModel.DoesNotExist:
        return Response({"error":"Todo item not found"},status=status.HTTP_404_NOT_FOUND)
    
    # checking if owner of todo item is request user or not
    if todo.owner != request.user:
        return Response({"error": "You do not have permission to access this todo item"}, status=status.HTTP_403_FORBIDDEN)

    #Handling GET request - sending todo detail as response 
    if request.method=='GET':
        try:
            serializer = TodoModelSerializer(todo)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except TodoModel.DoesNotExist:
            return Response({"error": "Todo item not found"}, status=status.HTTP_404_NOT_FOUND)
        
    # Handling PUT or PATCH request - updating the todo item
    if request.method in ['PUT','PATCH']:
    
        # retrieving fields (title,description and completed) from req body
        title = request.data.get('title',todo.title)
        description = request.data.get('description',todo.description)
        completed = request.data.get('completed',todo.completed)
        # serializing in the existing data 
        serializer = TodoModelSerializer(todo,data={"title":title,"description":description,"completed":completed})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    # Handling DELETE request - deleting todo item
    if request.method=='DELETE':
        if todo.delete():
            return Response({"message":"todo item deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    return Response({"error":"Bad request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    # serialize the request body
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # retrieve validated user
        user = serializer.validated_data['user']
        print(user)
        # get existing or create new token
        token,_ = Token.objects.get_or_create(user=user)
        return Response({"message":"Login Success","token":token.key})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    print(request.data)
    # serialize the request body
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        # save the user in database
        user = serializer.save()
        # get existing or create new token
        token,_ = Token.objects.get_or_create(user=user)
        return Response({"message":"Registration Success","token":token.key})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



