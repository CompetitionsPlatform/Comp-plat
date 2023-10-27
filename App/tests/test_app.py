import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
)

############################################################################################################
#A2 IMPORTS#################################################################################################
############################################################################################################
from App.models import RegularUser
from App.models import Admin
from App.models import Competition
from App.models import Result
from App.models import Roster

from App.controllers import(
    create_regular_user,
    is_user,
    get_user_by_id,
    toggle_registration,
    create_admin,
    is_admin,
    get_comp_by_id,
    create_competition,
    is_competition,
    delete_competition,
    get_all_comps,
    get_ranked,
    create_result,
)

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"


############################################################################################################
#A2 TESTS###################################################################################################
############################################################################################################
'''
TESTS REGULAR USERS
'''

class RegularUserUnitTests(unittest.TestCase):
    def test_new_user(self):
        user = RegularUser("bob", "bobpass")
        assert user.username == "bob"
    
    def test_toJSON_brief(self):
        user = RegularUser("bob", "bobpass")
        user_json = user.toJSON_brief()
        self.assertDictEqual(user_json, {'user_id': None, 'username': 'bob' ,'rank': 0})

    #need a function for the total json

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = RegularUser("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = RegularUser("bob", password)
        assert user.check_password(password)

class RegularUserIntegrationTests(unittest.TestCase):
    def test_create_regular_user(self):
        user = create_regular_user("bob", "bobpass")
        assert user.username == "bob"
    
    def test_is_user(self):
        assert (is_user(1)) != None
    
    def test_get_user_by_id(self):
        assert (get_user_by_id(1)) != None
    
    #error here
    def test_toggle_resigtration(self):
        new_admin = Admin("ron", "ronpass")
        new_comp = Competition(new_admin.id, "test_comp", "details", "2023-10-25 15:30:00.123456")
        new_user = create_regular_user("goob", "bobpass")
        
        new_roster = toggle_registration(new_user.id, new_comp.id)
        assert (new_roster.user_id) == new_user.id

'''
TESTS ADMIN
'''
class AdminUnitTests(unittest.TestCase):
    def test_new_admin(self):
        admin = Admin("ron","ronpass")
        assert admin.username == "ron"

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = Admin("bob", password)
        assert user.password != password
    
    def test_check_password(self):
        password = "mypass"
        user = Admin("rob", password)
        assert user.check_password(password)
    
    def test_toJSON(self):
        user = Admin("ron", "ronpass")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {'admin_id': None, 'username': 'ron' ,'admin_comps': []})

class AdminIntegrationTests(unittest.TestCase):
    def test_create_admin(self):
        admin = create_admin("gojo", "twoparts")
        assert admin.username == "gojo"
    
    def test_is_admin(self):
        admin = Admin("geto", "twobrains")
        assert (is_admin(admin.id)) != None

'''
COMPETITION TESTS
'''
class CompetitionUnitTests(unittest.TestCase):
    def test_new_comp(self):
        new_admin = Admin("rob", "robpass")
        new_comp = Competition(new_admin.id, "test_comp", "details", "2023-10-25 15:30:00.123456")
        assert new_comp.name == "test_comp"
        assert new_comp.details == "details"
        assert new_comp.event_date == "2023-10-25 15:30:00.123456"
    
    def test_toJson(self):
        new_admin = Admin("rob", "robpass")
        new_comp = Competition(new_admin.username, "test_comp", "details", "2023-10-25 15:30:00.123456")
        comp_json = new_comp.toJSON()
        self.assertDictEqual(comp_json, {'comp_id' : None, 
                                         'comp_name' : 'test_comp', 
                                         'comp_details': 'details', 
                                         'comp_date' : '2023-10-25 15:30:00.123456',
                                         'comp_admin_username' : None,
                                         'results': [],
                                         'registered_users': []})
    
    def test_toJSON_brief(self):
        new_admin = Admin("rob", "robpass")
        new_comp = Competition(new_admin.username, "test_comp", "details", "2023-10-25 15:30:00.123456")
        comp_json = new_comp.toJSON_brief()
        self.assertDictEqual(comp_json, {'comp_id': None,
                                         'comp_name': 'test_comp',
                                         'comp_details': 'details',
                                         'comp_date': '2023-10-25 15:30:00.123456',
                                         'comp_admin': None,})

class CompetitionIntegrationTests(unittest.TestCase):
    def test_create_competition(self):
        new_admin = create_admin("nanami", "isded")
        new_comp = create_competition(new_admin.id, "test_comp2", "details", "2023-10-25 15:30:00.123456")
        assert new_comp.name == "test_comp2"
    
    def test_get_comp_by_id(self):
        new_admin = create_admin("sleep", "isfortheweek")
        new_comp = create_competition(new_admin.id, "test_comp3", "details", "2023-10-25 15:30:00.123456")
        comp_search = get_comp_by_id(new_comp.id)
        assert comp_search.name == "test_comp3"

    def test_is_comp(self):
        new_admin = create_admin("python", "monty")
        new_comp = create_competition(new_admin.id, "test_comp4", "details", "2023-10-25 15:30:00.123456")
        res = is_competition(new_comp.name)
        assert new_comp.name == "test_comp4"
    
    def test_delete_comp(self):
        new_admin = create_admin("thiscouldbe", "easier")
        new_comp = create_competition(new_admin.id, "test_comp5", "details", "2023-10-25 15:30:00.123456")
        assert new_comp.name == "test_comp5"
        new_comp = delete_competition(new_comp.id)
        assert new_comp == None
    
    def test_get_all_comps(self):
        new_admin = create_admin("iwishthiswere", "easier")
        new_comp = create_competition(new_admin.id, "test_comp6", "details", "2023-10-25 15:30:00.123456")
        new_comp2 = create_competition(new_admin.id, "test_comp7", "details", "2023-10-25 15:30:00.123456")
        comps = get_all_comps()
        assert comps != None
    
    def test_get_ranked(self):
        user = create_regular_user("tom", "tompass")
        user2 = create_regular_user("dick", "dickpass")
        user3 = create_regular_user("harry", "harrypass")
        ranks = get_ranked()
        assert ranks != None
    
    def test_create_result(self):
        user = create_regular_user("tom", "tompass")
        admin = create_admin("lol", "ipop")
        comp = create_competition(admin.id, "test_comp8", "details", "2023-10-25 15:30:00.123456")
        res = create_result(comp.id, user.id, 99.9)
        assert res.comp_id == comp.id
        assert res.user_id == user.id
        assert res.score == 99.9

'''
RESULT TESTS
'''
class ResultUnitTests(unittest.TestCase):
    def test_result(self):
        new_result = Result(1, 2, 99.9)
        assert new_result.id == None
        assert new_result.comp_id == 1
        assert new_result.user_id == 2
        assert new_result.score == 99.9
    
    def test_toJSON(self):
        new_result = Result(1, 2, 99.9)
        result_json = new_result.toJSON()
        self.assertDictEqual(result_json, {'comp_id': 1,
                                           'user_id': 2,
                                           'score': 99.9,})
        
'''
ROSTER TESTS
'''
class RosterUnitTests(unittest.TestCase):
    def test_roster(self):
        new_roster = Roster(1, 2)
        assert new_roster.id == None
        assert new_roster.user_id == 1
        assert new_roster.comp_id == 2
