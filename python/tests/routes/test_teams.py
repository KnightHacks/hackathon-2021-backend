# flake8: noqa
import json
from src.models.hacker import Hacker
from src.models.user import ROLES
from src.models.team import Team
from tests.base import BaseTestCase


class TestTeamsBlueprint(BaseTestCase):
    """Tests for the Teams Endpoints"""

    """create_team (worked on by Conroy)"""

    def test_create_team(self):

        #create hackers to put inside team
        res1 = self.client.post(
            "/api/hackers/",
            data=json.dumps(
                {
                    "username": "conroy",
                    "email": "conroy@gmail.com",
                    "password": "fdsagfwedgasd",
                }
            ),
            content_type="application/json",
        )

        res2 = self.client.post(
            "/api/hackers/",
            data=json.dumps(
                {
                    "username": "john",
                    "email": "john@gmail.com",
                    "password": "fgnjmdsftgjh",
                }
            ),
            content_type="application/json",
        )

        res3 = self.client.post(
            "/api/hackers/",
            data=json.dumps(
                {
                    "username": "doe",
                    "email": "doe@gmail.com",
                    "password": "sdfghjk",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(res1.status_code, 201)
        self.assertEqual(res2.status_code, 201)
        self.assertEqual(res3.status_code, 201)
        self.assertEqual(Hacker.objects.count(), 3)

        #create a team
        res4 = self.client.post(
            "/api/teams/",
            data=json.dumps(
                {
                    "name" : "My Team",
                    "members" : [
                        "conroy@gmail.com",
                        "john@gmail.com",
                        "doe@gmail.com"],
                    "categories" : [
                        "category 1",
                        "category 2",
                        "category 3"]
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(res4.status_code, 201)
        self.assertEqual(Team.objects.count(), 1)

    def test_create_team_invalid_json(self):

        res4 = self.client.post(
            "/api/teams/",
            data=json.dumps({}),
            content_type="application/json",
        )

        self.assertEqual(res4.status_code, 400)
        self.assertEqual(Team.objects.count(), 0)

    def test_create_team_member_not_found(self):

        #create hackers to put inside team
        res1 = self.client.post(
            "/api/hackers/",
            data=json.dumps(
                {
                    "username": "conroy",
                    "email": "conroy@gmail.com",
                    "password": "fdsagfwedgasd",
                }
            ),
            content_type="application/json",
        )

        res2 = self.client.post(
            "/api/hackers/",
            data=json.dumps(
                {
                    "username": "john",
                    "email": "john@gmail.com",
                    "password": "fgnjmdsftgjh",
                }
            ),
            content_type="application/json",
        )

        res3 = self.client.post(
            "/api/hackers/",
            data=json.dumps(
                {
                    "username": "doe",
                    "email": "doe@gmail.com",
                    "password": "sdfghjk",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(res1.status_code, 201)
        self.assertEqual(res2.status_code, 201)
        self.assertEqual(res3.status_code, 201)
        self.assertEqual(Hacker.objects.count(), 3)

        #create a team
        res4 = self.client.post(
            "/api/teams/",
            data=json.dumps(
                {
                    "name" : "My Team",
                    "members" : [
                        "obviouslynotmyemail@gmail.com",
                        "john@gmail.com",
                        "doe@gmail.com"],
                    "categories" : [
                        "category 1",
                        "category 2",
                        "category 3"]
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(res4.status_code, 404)
        self.assertEqual(Team.objects.count(), 0)

    def test_create_team_duplicate_team(self):

        #create hackers to put inside teams
        res1 = self.client.post(
            "/api/hackers/",
            data=json.dumps(
                {
                    "username": "conroy",
                    "email": "conroy@gmail.com",
                    "password": "fdsagfwedgasd",
                }
            ),
            content_type="application/json",
        )

        res2 = self.client.post(
            "/api/hackers/",
            data=json.dumps(
                {
                    "username": "john",
                    "email": "john@gmail.com",
                    "password": "fgnjmdsftgjh",
                }
            ),
            content_type="application/json",
        )

        res3 = self.client.post(
            "/api/hackers/",
            data=json.dumps(
                {
                    "username": "doe",
                    "email": "doe@gmail.com",
                    "password": "sdfghjk",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(res1.status_code, 201)
        self.assertEqual(res2.status_code, 201)
        self.assertEqual(res3.status_code, 201)
        self.assertEqual(Hacker.objects.count(), 3)

        #create teams
        res4 = self.client.post(
            "/api/teams/",
            data=json.dumps(
                {
                    "name" : "My Team",
                    "members" : [
                        "conroy@gmail.com",
                        "john@gmail.com"],
                    "categories" : [
                        "category 1",
                        "category 2",
                        "category 3"]
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(res4.status_code, 201)
        self.assertEqual(Team.objects.count(), 1)

        res5 = self.client.post(
            "/api/teams/",
            data=json.dumps(
                {
                    "name" : "My Team",
                    "members" : [
                        "doe@gmail.com"],
                    "categories" : [
                        "category 1",
                        "category 2",
                        "category 3"]
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(res5.status_code, 409)
        self.assertEqual(Team.objects.count(), 1)

    def test_create_team_invalid_datatypes(self):

        #create hackers to put inside team
        res1 = self.client.post(
            "/api/hackers/",
            data=json.dumps(
                {
                    "username": "conroy",
                    "email": "conroy@gmail.com",
                    "password": "fdsagfwedgasd",
                }
            ),
            content_type="application/json",
        )

        res2 = self.client.post(
            "/api/hackers/",
            data=json.dumps(
                {
                    "username": "john",
                    "email": "john@gmail.com",
                    "password": "fgnjmdsftgjh",
                }
            ),
            content_type="application/json",
        )

        res3 = self.client.post(
            "/api/hackers/",
            data=json.dumps(
                {
                    "username": "doe",
                    "email": "doe@gmail.com",
                    "password": "sdfghjk",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(res1.status_code, 201)
        self.assertEqual(res2.status_code, 201)
        self.assertEqual(res3.status_code, 201)
        self.assertEqual(Hacker.objects.count(), 3)

        #create a team
        res4 = self.client.post(
            "/api/teams/",
            data=json.dumps(
                {
                    "name" : 2142114,
                    "members" : [
                        "conroy@gmail.com",
                        "john@gmail.com",
                        "doe@gmail.com"],
                    "categories" : [
                        "category 1",
                        "category 2",
                        "category 3"]
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(res4.status_code, 400)
        self.assertEqual(Team.objects.count(), 0)

    """edit_team (worked on by Conroy)"""

    def test_edit_team(self):

        #create hackers to put inside team
        new_hacker1 = Hacker.createOne(
            first_name = "Conroy",
            username = "conroy",
            email = "conroy@gmail.com",
            password = "dsafadsgdasg",
            roles = ROLES.HACKER
        )

        new_hacker2 = Hacker.createOne(
            first_name = "John",
            username = "john",
            email = "john@gmail.com",
            password = "fgnjmdsftgjh",
            roles = ROLES.HACKER
        )

        new_hacker3 = Hacker.createOne(
            first_name = "Doe",
            username = "doe",
            email = "doe@gmail.com",
            password = "sdfghjk",
            roles = ROLES.HACKER
        )

        #create a team
        new_team = Team.createOne(
            name = "My Team",
            members = [
                        new_hacker1,
                        new_hacker2,
                        new_hacker3],
            categories = [
                        "category 1",
                        "category 2",
                        "category 3"]
        )

        #edit team
        res = self.client.put(
            "/api/teams/My Team/",
            data=json.dumps({"name": "My Updated Team",
                             "members": [
                                        "conroy@gmail.com",
                                        "john@gmail.com",
                                        "doe@gmail.com"]}),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 201)


    def test_edit_team_invalid_json(self):

        #create hackers to put inside team
        new_hacker1 = Hacker.createOne(
            first_name = "Conroy",
            username = "conroy",
            email = "conroy@gmail.com",
            password = "dsafadsgdasg",
            roles = ROLES.HACKER
        )

        new_hacker2 = Hacker.createOne(
            first_name = "John",
            username = "john",
            email = "john@gmail.com",
            password = "fgnjmdsftgjh",
            roles = ROLES.HACKER
        )

        new_hacker3 = Hacker.createOne(
            first_name = "Doe",
            username = "doe",
            email = "doe@gmail.com",
            password = "sdfghjk",
            roles = ROLES.HACKER
        )

        #create a team
        new_team = Team.createOne(
            name = "My Team",
            members = [
                        new_hacker1,
                        new_hacker2,
                        new_hacker3],
            categories = [
                        "category 1",
                        "category 2",
                        "category 3"]
        )

        #edit team
        res = self.client.put(
            "/api/teams/My Team/",
            data=json.dumps({}),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400)

    def test_edit_team_not_found(self):

        #create hackers to put inside team
        new_hacker1 = Hacker.createOne(
            first_name = "Conroy",
            username = "conroy",
            email = "conroy@gmail.com",
            password = "dsafadsgdasg",
            roles = ROLES.HACKER
        )

        new_hacker2 = Hacker.createOne(
            first_name = "John",
            username = "john",
            email = "john@gmail.com",
            password = "fgnjmdsftgjh",
            roles = ROLES.HACKER
        )

        new_hacker3 = Hacker.createOne(
            first_name = "Doe",
            username = "doe",
            email = "doe@gmail.com",
            password = "sdfghjk",
            roles = ROLES.HACKER
        )

        #create a team
        new_team = Team.createOne(
            name = "My Team",
            members = [
                        new_hacker1,
                        new_hacker2,
                        new_hacker3],
            categories = [
                        "category 1",
                        "category 2",
                        "category 3"]
        )

        #edit team
        res = self.client.put(
            "/api/teams/Not My Team/",
            data=json.dumps({"name": "My Updated Team",
                             "members": [
                                        "conroy@gmail.com",
                                        "john@gmail.com",
                                        "doe@gmail.com"]}),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 404)

    def test_edit_team_member_not_found(self):

        #create hackers to put inside team
        new_hacker1 = Hacker.createOne(
            first_name = "Conroy",
            username = "conroy",
            email = "conroy@gmail.com",
            password = "dsafadsgdasg",
            roles = ROLES.HACKER
        )

        new_hacker2 = Hacker.createOne(
            first_name = "John",
            username = "john",
            email = "john@gmail.com",
            password = "fgnjmdsftgjh",
            roles = ROLES.HACKER
        )

        new_hacker3 = Hacker.createOne(
            first_name = "Doe",
            username = "doe",
            email = "doe@gmail.com",
            password = "sdfghjk",
            roles = ROLES.HACKER
        )

        #create a team
        new_team = Team.createOne(
            name = "My Team",
            members = [
                        new_hacker1,
                        new_hacker2,
                        new_hacker3],
            categories = [
                        "category 1",
                        "category 2",
                        "category 3"]
        )

        #edit team
        res = self.client.put(
            "/api/teams/My Team/",
            data=json.dumps({"name": "My Updated Team",
                             "members": [
                                        "obviouslynotmyemail@gmail.com",
                                        "john@gmail.com",
                                        "doe@gmail.com"]}),
            content_type="application/json"
        )

        self.assertEqual(res.status_code, 404)

    def test_edit_team_duplicate_team(self):

        #create hackers to put inside team
        new_hacker1 = Hacker.createOne(
            first_name = "Conroy",
            username = "conroy",
            email = "conroy@gmail.com",
            password = "dsafadsgdasg",
            roles = ROLES.HACKER
        )

        new_hacker2 = Hacker.createOne(
            first_name = "John",
            username = "john",
            email = "john@gmail.com",
            password = "fgnjmdsftgjh",
            roles = ROLES.HACKER
        )

        new_hacker3 = Hacker.createOne(
            first_name = "Doe",
            username = "doe",
            email = "doe@gmail.com",
            password = "sdfghjk",
            roles = ROLES.HACKER
        )

        #create teams
        new_team1 = Team.createOne(
            name = "Team 1",
            members = [
                        new_hacker1,
                        new_hacker2,
                        new_hacker3],
            categories = [
                        "category 1",
                        "category 2",
                        "category 3"]
        )

        new_team2 = Team.createOne(
            name = "Team 2",
            members = [
                        new_hacker1,
                        new_hacker2,
                        new_hacker3],
            categories = [
                        "category 1",
                        "category 2",
                        "category 3"]
        )

        #edit a team
        res = self.client.put(
            "/api/teams/Team 1/",
            data=json.dumps({"name": "Team 2",
                             "members": [
                                        "conroy@gmail.com",
                                        "john@gmail.com",
                                        "doe@gmail.com"]}),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 409)

    def test_edit_team_invalid_datatypes(self):

        #create hackers to put inside team
        new_hacker1 = Hacker.createOne(
            first_name = "Conroy",
            username = "conroy",
            email = "conroy@gmail.com",
            password = "dsafadsgdasg",
            roles = ROLES.HACKER
        )

        new_hacker2 = Hacker.createOne(
            first_name = "John",
            username = "john",
            email = "john@gmail.com",
            password = "fgnjmdsftgjh",
            roles = ROLES.HACKER
        )

        new_hacker3 = Hacker.createOne(
            first_name = "Doe",
            username = "doe",
            email = "doe@gmail.com",
            password = "sdfghjk",
            roles = ROLES.HACKER
        )

        #create a team
        new_team = Team.createOne(
            name = "My Team",
            members = [
                        new_hacker1,
                        new_hacker2,
                        new_hacker3],
            categories = [
                        "category 1",
                        "category 2",
                        "category 3"]
        )

        #edit team
        res = self.client.put(
            "/api/teams/My Team/",
            data=json.dumps({"name": 1,
                             "members": [
                                        "conroy@gmail.com",
                                        "john@gmail.com",
                                        "doe@gmail.com"]}),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400)

    """get_team (worked on by Conroy)"""

    def test_get_team(self):

        #create hackers to put inside team
        new_hacker1 = Hacker.createOne(
            first_name = "Conroy",
            username = "conroy",
            email = "conroy@gmail.com",
            password = "dsafadsgdasg",
            roles = ROLES.HACKER
        )

        new_hacker2 = Hacker.createOne(
            first_name = "John",
            username = "john",
            email = "john@gmail.com",
            password = "fgnjmdsftgjh",
            roles = ROLES.HACKER
        )

        new_hacker3 = Hacker.createOne(
            first_name = "Doe",
            username = "doe",
            email = "doe@gmail.com",
            password = "sdfghjk",
            roles = ROLES.HACKER
        )

        #create a team
        new_team = Team.createOne(
            name = "My Team",
            members = [
                        new_hacker1,
                        new_hacker2,
                        new_hacker3],
            categories = [
                        "category 1",
                        "category 2",
                        "category 3"]
        )

        #get the team
        res = self.client.get("/api/teams/My Team/")
        self.assertEqual(res.status_code, 200)

    def test_get_team_not_found(self):

        #create hackers to put inside team
        new_hacker1 = Hacker.createOne(
            first_name = "Conroy",
            username = "conroy",
            email = "conroy@gmail.com",
            password = "dsafadsgdasg",
            roles = ROLES.HACKER
        )

        new_hacker2 = Hacker.createOne(
            first_name = "John",
            username = "john",
            email = "john@gmail.com",
            password = "fgnjmdsftgjh",
            roles = ROLES.HACKER
        )

        new_hacker3 = Hacker.createOne(
            first_name = "Doe",
            username = "doe",
            email = "doe@gmail.com",
            password = "sdfghjk",
            roles = ROLES.HACKER
        )

        #create a team
        new_team = Team.createOne(
            name = "My Team",
            members = [
                        new_hacker1,
                        new_hacker2,
                        new_hacker3],
            categories = [
                        "category 1",
                        "category 2",
                        "category 3"]
        )

        #"get" the team
        res = self.client.get("/api/teams/Obviously Not My Team/")
        self.assertEqual(res.status_code, 404)
