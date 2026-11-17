from . import placement
from . import invitations
from . import registration

OPERATIONS={
    'placement.request':placement.request,
    'invitations.invite':invitations.invite,
    'registration.accept':registration.accept,
}
