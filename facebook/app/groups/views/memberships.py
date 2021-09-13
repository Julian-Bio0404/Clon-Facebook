"""Membership views."""

# Django
from django.utils import timezone

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from groups.models import Group, Membership, Invitation
from users.models import User

# Serializers
from groups.serializers import MembershipModelSerializer, AddMemberSerializer


class MembershipViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Group membership view set."""

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the group exists."""
        slug_name = kwargs['slug_name']
        self.group = get_object_or_404(Group, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return group members."""
        return Membership.objects.filter(group=self.group, is_active=True)

    def get_object(self):
        """Return the group member by using the user's username."""
        return get_object_or_404(
            Membership, user__username=self.kwargs['pk'], group=self.group)
    
    def perform_destroy(self, instance):
        """Delete a membership and invitation."""
        user = instance.user
        group = instance.group
        invitation = get_object_or_404(Invitation, used_by=user, group=group)
        invitation.delete()
        instance.delete()

    def create(self, request, *args, **kwargs):
        """Handle member creation from invitation code."""
        serializer = AddMemberSerializer(
            data=request.data, context={'group': self.group, 'request': request})
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        data = self.get_serializer(member).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def invitations(self, request, *args, **kwargs):
        """Create a invitation."""
        username = request.data['username']

        try:
            guest_user = User.objects.get(username=username)
            invitation = Invitation.objects.create(
                sent_by=request.user, used_by=guest_user, group=self.group).code
            data = {
                'message': f'You invited {guest_user.username} to join the {self.group.slug_name} group.',
                'invitation code': invitation}
            return Response(data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            data = {'message': "The user doesn't exist."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def confirm_invitation(self, request, *args, **kwargs):
        """Confirm gropup's invitation."""
        code = request.data['invitation_code']

        try:
            # Invitation
            invitation = Invitation.objects.get(code=code)
            invitation.used = True
            invitation.used_at = timezone.now()
            invitation.save()

            serializer = AddMemberSerializer(
                data=request.data, 
                context={'group': self.group, 'request': request, 'user': request.user })
            serializer.is_valid(raise_exception=True)
            membership = serializer.save()
            data = MembershipModelSerializer(membership).data
            return Response(data, status=status.HTTP_201_CREATED)
        except Invitation.DoesNotExist:
            data = {'message': 'Invalid invitation.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def confirm_membership(self, request, *args, **kwargs):
        """Confirm group's membership by admin."""
        if request.data['accepted'] == True:
            membership =  self.get_object()
            membership.is_active = True
            membership.save()
            data = MembershipModelSerializer(membership).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': 'You do not confirm the membership yet.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
