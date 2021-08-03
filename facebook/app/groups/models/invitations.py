"""Group invitation model."""

# Django
from django.db import models

# Utilities
from utils.models import FbModel

# Managers
from groups.managers.invitations import InvitationManager


class Invitation(FbModel):
    """Group invitation.

    A group invitation is a random text that acts as 
    a unique code that grants access to a specific group.
    This codes are generated by users that are already
    members of the group.
    """

    code = models.CharField(max_length=50, unique=True)

    sent_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        help_text='Group member that is providing the invitation',
    )

    used_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        help_text='User that used the code to enter the group',
        related_name='used_by'
    )

    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE)

    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(blank=True, null=True)

    # Manager
    objects = InvitationManager()
    
    def __str__(self):
        """Return code and circle."""
        return "#{}: {}".format(self.group.slug_name, self.code)