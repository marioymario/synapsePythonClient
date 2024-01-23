from synapseclient.models.user import UserGroupHeader


class TestUserGroupHeader:
    def test_fill_from_dict(self):
        test_dict = {
            "ownerId": 123,
            "firstName": "John",
            "lastName": "Doe",
            "userName": "jdoe",
            "email": "jdoe@me.com",
            "isIndividual": True,
        }
        user_group_header = UserGroupHeader()
        user_group_header.fill_from_dict(test_dict)
        assert user_group_header.owner_id == 123
        assert user_group_header.first_name == "John"
        assert user_group_header.last_name == "Doe"
        assert user_group_header.user_name == "jdoe"
        assert user_group_header.email == "jdoe@me.com"
        assert user_group_header.is_individual == True
