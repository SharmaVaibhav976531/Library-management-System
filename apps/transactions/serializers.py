from rest_framework import serializers
from .models import BookIssue, Reservation, Fine, Member
from apps.library.models import Book

class IssueBookSerializer(serializers.Serializer):
    member_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    def validate(self, data):
        member = Member.objects.get(id=data['member_id'])
        book = Book.objects.get(id=data['book_id'])
        if member.status != 'active':
            raise serializers.ValidationError("Membership inactive.")
        if book.available_copies <= 0:
            raise serializers.ValidationError("No copies available.")
        overdue = BookIssue.objects.filter(member=member, status='overdue').count()
        if overdue >= 2:
            raise serializers.ValidationError("Member has 2+ overdue books.")
        return data
