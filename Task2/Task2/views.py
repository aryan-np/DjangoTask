from rest_framework.response import Response
from .serializers import TodoModelSerializer
from .models import TodoModel
from rest_framework.decorators import api_view
from rest_framework import status
@api_view(['GET'])
def getTodoList(request):
    lists = TodoModel.objects.all()
    serializer = TodoModelSerializer(lists,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTodoDetail(request, id):
    try:
        todo = TodoModel.objects.get(id=id)
        serializer = TodoModelSerializer(todo)
        return Response(serializer.data)
    except TodoModel.DoesNotExist:
        return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

 


@api_view(['POST'])
def createTodo(request):
    title = request.data.get('title')
    description = request.data.get('description')
    
    if not title or not description:
        return Response({'error': 'Both title and description are required'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = TodoModelSerializer(data={"title":title,"description":description})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT','PATCH'])
def updateTodo(request,id):
    if not id:
        return Response({"error":"Missing todo id"},status=status.HTTP_404_NOT_FOUND)
    try:
        todo = TodoModel.objects.get(id=id)
    except TodoModel.DoesNotExist:
        return Response({"error":"Todo item not found"},status=status.HTTP_404_NOT_FOUND)
    title = request.data.get('title',todo.title)
    description = request.data.get('description',todo.description)
    serializer = TodoModelSerializer(todo,data={"title":title,"description":description})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteTodo(request,id):
    if not id:
        return Response({"error":"Missing todo id"},status=status.HTTP_404_NOT_FOUND)
    try:
        todo = TodoModel.objects.get(id=id)
    except TodoModel.DoesNotExist:
        return Response({"error":"Todo item not found"},status=status.HTTP_404_NOT_FOUND)
    if todo.delete():
        return Response({"message":"todo item deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    return Response({"error":"Bad request"}, status=status.HTTP_400_BAD_REQUEST)