from rest_framework.response import Response
from .serializers import TodoModelSerializer
from .models import TodoModel
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET','POST'])
def getAndCreateTodo(request):
    # return all list if method is get
    if request.method=='GET':
        # retrieving all list and serializing into json
        lists = TodoModel.objects.all()
        serializer = TodoModelSerializer(lists,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # if request method is post create new todo item
    if request.method=='POST':
        # retrieve title and description from req body
        title = request.data.get('title')
        description = request.data.get('description')
        
        if not title or not description:
            return Response({'error': 'Both title and description are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        #serializing the data and saving it  
        serializer = TodoModelSerializer(data={"title":title,"description":description})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        




@api_view(['GET','PUT','PATCH','DELETE'])
def getUpdateOrDeleteTodo(request, id):
    # retrieced id from path parameter
    if not id:
        return Response({"error":"Missing todo id"},status=status.HTTP_404_NOT_FOUND)
    
    # checking if todo with retrieved exists
    try:
        todo = TodoModel.objects.get(id=id)
    except TodoModel.DoesNotExist:
        return Response({"error":"Todo item not found"},status=status.HTTP_404_NOT_FOUND)
    
    #if request method is get sending todo detail as response 
    if request.method=='GET':
        try:
            serializer = TodoModelSerializer(todo)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except TodoModel.DoesNotExist:
            return Response({"error": "Todo item not found"}, status=status.HTTP_404_NOT_FOUND)
        
    # if the request method is put or patch updating the todo item
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
    
    # if request method is delete deleting the todo item
    if request.method=='DELETE':
        if todo.delete():
            return Response({"message":"todo item deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    return Response({"error":"Bad request"}, status=status.HTTP_400_BAD_REQUEST)



