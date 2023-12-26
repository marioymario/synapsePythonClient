from dataclasses import dataclass
from opentelemetry import trace

tracer = trace.get_tracer("synapseclient")


@dataclass
class Permissions:
    """The permission a User has for a given Entity.


    Attributes:
        can_view : Can the user view this entity?
        can_edit : Can the user edit this entity?
        can_move : (Read Only) Can the user move this entity by changing its parentId?
        can_add_child : Can the user add a child entity to this entity?
        can_certified_user_edit : (Read Only) Can the user edit this entity once they become a Certified User?
        can_certified_user_add_child : (Read Only) Can the user add a child entity to this entity once they become a Certified User?
        is_certified_user : (Read Only) True, if the user has passed the user certification quiz.
        can_change_permissions : Can the user change the permissions of this entity?
        can_change_settings : Can the user change the settings of this entity?
        can_delete : Can the user delete this entity?
        can_download : Are there any access requirements precluding the user from downloading this entity?
        can_upload : (Read Only) Are there any access requirements precluding the user from uploading into this entity (folder or project)?
        can_enable_inheritance : (Read Only) Can the user delete the entity's access control list (so it inherits settings from an ancestor)?
        owner_principal_id : (Read Only) The principal ID of the entity's owner (i.e. the entity's 'createdBy')
        can_public_read : (Read Only) Is this entity considered public?
        can_moderate : Can the user moderate the forum associated with this entity? Note that only project entity has forum.
        is_certification_required : (Read Only) Is the certification requirement enabled for the project of the entity?
        is_entity_open_data : (Read Only) Returns true if the Entity's DateType equals 'OPEN_DATA', indicating that the data is safe to be released to the public.
    """

    can_view: bool = None
    """Can the user view this entity?"""

    can_edit: bool = None
    """Can the user edit this entity?"""

    can_move: bool = None
    """(Read Only) Can the user move this entity by changing its parentId?"""

    can_add_child: bool = None
    """Can the user add a child entity to this entity?"""

    can_certified_user_edit: bool = None
    """(Read Only) Can the user edit this entity once they become a Certified User?"""

    can_certified_user_add_child: bool = None
    """(Read Only) Can the user add a child entity to this entity once they become a Certified User?"""

    is_certified_user: bool = None
    """(Read Only) True, if the user has passed the user certification quiz."""

    can_change_permissions: bool = None
    """Can the user change the permissions of this entity?"""

    can_change_settings: bool = None
    """Can the user change the settings of this entity?"""

    can_delete: bool = None
    """Can the user delete this entity?"""

    can_download: bool = None
    """Are there any access requirements precluding the user from downloading this entity?"""

    can_upload: bool = None
    """(Read Only) Are there any access requirements precluding the user from uploading into this entity (folder or project)?"""

    can_enable_inheritance: bool = None
    """(Read Only) Can the user delete the entity's access control list (so it inherits settings from an ancestor)?"""

    owner_principal_id: int = None
    """(Read Only) The principal ID of the entity's owner (i.e. the entity's 'createdBy')"""

    can_public_read: bool = None
    """(Read Only) Is this entity considered public?"""

    can_moderate: bool = None
    """Can the user moderate the forum associated with this entity? Note that only project entity has forum."""

    is_certification_required: bool = None
    """(Read Only) Is the certification requirement enabled for the project of the entity?"""

    is_entity_open_data: bool = None
    """(Read Only) Returns true if the Entity's DateType equals 'OPEN_DATA', indicating that the data is safe to be released to the public."""

    @classmethod
    def from_dict(cls, data: dict) -> "Permissions":
        """Convert a data dictionary to an instance of this dataclass

        Arguments:
            data: a data dictionary of the [UserEntityPermissions](https://rest-docs.synapse.org/rest/org/sagebionetworks/repo/model/auth/UserEntityPermissions.html)

        Returns:
            A Permission object
        """

        return cls(
            can_view=data["canView"],
            can_edit=data["canEdit"],
            can_move=data["canMove"],
            can_add_child=data["canAddChild"],
            can_certified_user_edit=data["canCertifiedUserEdit"],
            can_certified_user_add_child=data["canCertifiedUserAddChild"],
            is_certified_user=data["isCertifiedUser"],
            can_change_permissions=data["canChangePermissions"],
            can_change_settings=data["canChangeSettings"],
            can_delete=data["canDelete"],
            can_download=data["canDownload"],
            can_upload=data["canUpload"],
            can_enable_inheritance=data["canEnableInheritance"],
            owner_principal_id=data["ownerPrincipalId"],
            can_public_read=data["canPublicRead"],
            can_moderate=data["canModerate"],
            is_certification_required=data["isCertificationRequired"],
            is_entity_open_data=data["isEntityOpenData"],
        )

    @property
    def access_types(self):
        """
        Determine from the permissions set on this object what the access types are.

        Returns:
            A list of access type strings for this object based off of what permissions are set.


        Example: Using this property
            A permission that has nothing set

                no_permissions = Permissions()
                print(no_permissions.access_types)
                # Prints: []

            A permission that has can_view set to True and nothing else set

                read_permission = Permissions()
                read_permission.can_view = True
                print(read_permission.access_types)
                # Prints: ['READ']

            Special Case: a permission that has can_view set to True and nothing else set on an entity created by you.
            CHANGE_SETTINGS is bound to ownerId. Since the entity is created by you, the CHANGE_SETTINGS will always be True.
               read_permission = Permissions()
               read_permission.can_view = True
               print(read_permission.access_types)
               # Prints: ['READ','CHANGE_SETTINGS']

            A permission that has can_view and can_edit set to True and nothing else set

                read_write_permission = Permissions()
                read_write_permission.can_view = True
                read_write_permission.can_edit = True
                print(read_write_permission.access_types)
                # Prints: ['READ', 'UPDATE']
        """

        access_types = []
        if self.can_view:
            access_types.append("READ")
        if self.can_edit:
            access_types.append("UPDATE")
        if self.can_add_child:
            access_types.append("CREATE")
        if self.can_delete:
            access_types.append("DELETE")
        if self.can_download:
            access_types.append("DOWNLOAD")
        if self.can_moderate:
            access_types.append("MODERATE")
        if self.can_change_permissions:
            access_types.append("CHANGE_PERMISSIONS")
        if self.can_change_settings:
            access_types.append("CHANGE_SETTINGS")
        return access_types
