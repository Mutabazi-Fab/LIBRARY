from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, User, Transaction
from .serializers import BookSerializer, UserSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        books = Book.objects.filter(number_of_copies_available__gt=0)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def checkout(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        book = Book.objects.get(id=book_id)

        if book.number_of_copies_available > 0:
            book.number_of_copies_available -= 1
            book.save()
            transaction = Transaction.objects.create(user=user, book=book)
            return Response({'message': 'Book checked out successfully.', 'transaction': TransactionSerializer(transaction).data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'No available copies.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def return_book(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        book = Book.objects.get(id=book_id)
        transaction = Transaction.objects.filter(user=user, book=book, return_date__isnull=True).first()

        if transaction:
            transaction.return_date = timezone.now()
            transaction.save()
            book.number_of_copies_available += 1
            book.save()
            return Response({'message': 'Book returned successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No active checkout found for this book.'}, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})