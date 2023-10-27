import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

############################################################################################################
#A2 TESTS###################################################################################################
############################################################################################################

regUsrTests = AppGroup('regUserTest', help="run regular user tests")
@regUsrTests.command("regUser", help="Run Regular User tests")
@click.argument("type", default="all")
def reg_user_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "RegularUserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "RegularUserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(regUsrTests)

adminTests = AppGroup("adminTests", help="run admin tests")
@adminTests.command("admin", help="run admin tests")
@click.argument("type", default="all")
def admin_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "AdminUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "AdminIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(adminTests)

competitionTests = AppGroup("competitionTests", help="run competition tests")
@competitionTests.command("comp", help="run competition tests")
@click.argument("type", default="all")
def competition_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "CompetitionUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "CompetitionIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(competitionTests)

resultTests = AppGroup("resultTests", help="run result tests")
@resultTests.command("result", help="run result tests")
@click.argument("type", default="all")
def result_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "ResultUnitTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(resultTests)

rosterTests = AppGroup("rosterTests", help="run roster tests")
@rosterTests.command("roster", help="run roster tests")
@click.argument("type", default="all")
def roster_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "RosterUnitTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(rosterTests)
