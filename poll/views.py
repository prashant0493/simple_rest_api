from django.contrib.auth.models import User


from poll.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render


class UserList(APIView):
    """
    List all users, or create a new user
    """

    def get(self, request, format=None):
        print('get() method from UserList is being executed...')
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        data = serializer.data
        profiles = [item['username'] for item in data]
        return render(request, 'poll/index.html', {'profiles' :profiles, 'profiles_len':len(profiles)})
        # return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        print("GET request in my bucket --")
        user = self.get_object(pk)
        user = UserSerializer(user)
        data = user.data
        print("data - {}, data['username'] - {}".format(data, data['username']))
        return render(request, 'poll/index.html', {'profiles' :data['username'], 'profiles_len': 1})
        # return Response(user.data)
    '''
    def get(self, request):
        user = User.objects.all()
        print(dir(user))
        user = user.first()
        user = UserSerializer(user)
        return Response(user.data)
   ''' 

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
