# flake8: noqa
import json
from src.models.sponsor import Sponsor
from tests.base import BaseTestCase
from src.models.user import ROLES


class TestSponsorsBlueprint(BaseTestCase):
    """Tests for the Sponsors Endpoints"""

    """create_sponsor (worked on by Conroy) """

    def test_create_sponsor(self):
        
        #resemble someone using the create sponsor route to make a new sponsor
        res = self.client.post(
            "/api/sponsors/",
            data = json.dumps({
                "sponsor_name" : "Bose",
                "logo" : "https://blob.knighthacks.org/somelogo.png",
                "subscription_tier" : "Gold",
                "email" : "bose@gmail.com",
                "username" : "boseofficial",
                "password" : "pass1234"
            }),
            content_type="application/json")

        #ensure that the sponsor was successfully created
        self.assertEqual(res.status_code, 201)

        #ensure that a sponsor object exists in MonogDB
        self.assertEqual(Sponsor.objects.count(), 1)

    def test_create_sponsor_invalid_json(self):
        
        #resemble someone using the create sponsor route to make a new sponsor but with no data (i.e. an empty json)
        res = self.client.post(
            "/api/sponsors/",
            data = json.dumps({}),
            content_type="application/json")

        #ensure that the sponsor was unsuccessfully created (due to invalid json file)
        self.assertEqual(res.status_code, 400)

        #ensure that no sponsor objects exist in MonogDB
        self.assertEqual(Sponsor.objects.count(), 0)

    def test_create_sponsor_not_unique(self):
        
        #resemble someone using the create sponsor route to make a new sponsor
        res = self.client.post(
            "/api/sponsors/",
            data = json.dumps({
                "sponsor_name" : "Bose",
                "logo" : "https://blob.knighthacks.org/somelogo.png",
                "subscription_tier" : "Gold",
                "email" : "bose@gmail.com",
                "username" : "boseofficial",
                "password" : "pass1234"
            }),
            content_type="application/json")

        #ensure that the sponsor was successfully created
        self.assertEqual(res.status_code, 201)

        #resemble someone using the create sponsor route to make another new sponsor but with a non-unique username
        res2 = self.client.post(
            "/api/sponsors/",
            data = json.dumps({
                "sponsor_name" : "Amazon",
                "logo" : "https://blob.knighthacks.org/somelogo.png",
                "subscription_tier" : "Gold",
                "email" : "amazon@gmail.com",
                "username" : "boseofficial",
                "password" : "pass1234"
            }),
            content_type="application/json")

        #ensure that the sponsor was unsuccessfully created due to not being unique
        self.assertEqual(res2.status_code, 409)

        #ensure that only 1 sponsor object exists in MonogDB
        self.assertEqual(Sponsor.objects.count(), 1)

    def test_create_sponsor_invalid_datatype(self):
        
        #resemble someone using the create sponsor route to make a new sponsor but with an invalid datatype for the email
        res = self.client.post(
            "/api/sponsors/",
            data = json.dumps({
                "sponsor_name" : "Google",
                "logo" : "https://blob.knighthacks.org/somelogo.png",
                "subscription_tier" : "Gold",
                "email" : 123,
                "username" : "googleofficial",
                "password" : "pass1234"
            }),
            content_type="application/json")

        #ensure that the sponsor was unsuccessfully created due to an invalid datatype
        self.assertEqual(res.status_code, 400)

        #ensure that no sponsor objects exist in MonogDB
        self.assertEqual(Sponsor.objects.count(), 0)


    """delete_sponsor (worked on by Simon and Conroy)"""

    def test_delete_sponsor(self):
        Sponsor.createOne(username="foobar",
                          sponsor_name="foobar",
                          email="foobar@email.com",
                          password="123456",
                          roles=ROLES.SPONSOR)

        token = self.login_user(ROLES.ADMIN)

        res = self.client.delete("/api/sponsors/delete_sponsor/foobar/",
                                 headers=[("sid", token)])

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Sponsor.objects.count(), 0)

    def test_delete_sponsor_as_self(self):
        sponsor = Sponsor.createOne(username="foobar",
                          sponsor_name="foobar",
                          email="foobar@email.com",
                          password="123456",
                          roles=ROLES.SPONSOR)

        token = sponsor.encode_auth_token()

        res = self.client.delete("/api/sponsors/delete_sponsor/foobar/",
                                 headers=[("sid", token)])

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Sponsor.objects.count(), 0)

    def test_delete_sponsor_as_other_sponsor(self):
        Sponsor.createOne(username="foobar",
                          sponsor_name="foobar",
                          email="foobar@email.com",
                          password="123456",
                          roles=ROLES.SPONSOR)

        other_sponsor = Sponsor.createOne(username="tester",
                                          sponsor_name="tester",
                                          email="tester@email.com",
                                          password="123456",
                                          roles=ROLES.SPONSOR)

        token = other_sponsor.encode_auth_token()

        res = self.client.delete("/api/sponsors/delete_sponsor/foobar/",
                                 headers=[("sid", token)])

        self.assertEqual(res.status_code, 401)

    def test_delete_sponsor_not_found(self):

        #create a new sponsor document in MongoDB
        Sponsor.createOne(sponsor_name = "Bose",
                          logo = "https://blob.knighthacks.org/somelogo.png",
                          subscription_tier = "Gold",
                          email = "bose@gmail.com",
                          username = "boseofficial",
                          password = "pass1234",
                          roles = ROLES.SPONSOR)
        
        #resemble someone using the delete sponsor route to delete the one that we just created but they used the wrong name
        token = self.login_user(ROLES.ADMIN)
        res = self.client.delete("/api/sponsors/delete_sponsor/Boses/",
                                 headers=[("sid", token)])

        #ensure that the sponsor was unsuccessfully deleted due to incorrect name
        self.assertEqual(res.status_code, 404)

        #ensure that 1 sponsor object exists in MonogDB
        self.assertEqual(Sponsor.objects.count(), 1)

    """get_sponsor (worked on by Conroy)"""

    def test_get_sponsor(self):
        
        #create a new sponsor document in MongoDB
        new_sponsor = Sponsor.createOne(
                          sponsor_name = "Bose",
                          logo = "https://blob.knighthacks.org/somelogo.png",
                          subscription_tier = "Gold",
                          email = "bose@gmail.com",
                          username = "boseofficial",
                          password = "pass1234",
                          roles = ROLES.SPONSOR)

        #resemble someone using the get sponsor route to get the sponsor that we created
        res = self.client.get("/api/sponsors/Bose/")   

        #ensure that we successfully got the sponsor
        self.assertEqual(res.status_code, 200)

    def test_get_sponsor_not_found(self):
        
        #create a new sponsor document in MongoDB
        new_sponsor = Sponsor.createOne(
                          sponsor_name = "Bose",
                          logo = "https://blob.knighthacks.org/somelogo.png",
                          subscription_tier = "Gold",
                          email = "bose@gmail.com",
                          username = "boseofficial",
                          password = "pass1234",
                          roles = ROLES.SPONSOR)

        #resemble someone using the get sponsor route to get the sponsor that we created but they used the wrong name
        res = self.client.get("/api/sponsors/Boses/")    

        #ensure that we unsuccessfully got the sponsor due to an incorrect name
        self.assertEqual(res.status_code, 404)


    """edit_sponsor (worked on by Conroy)"""

    def test_edit_sponsor(self):
        
        #create a new sponsor document in MongoDB
        Sponsor.createOne(sponsor_name = "Bose",
                          logo = "https://blob.knighthacks.org/somelogo.png",
                          subscription_tier = "Gold",
                          email = "bose@gmail.com",
                          username = "boseofficial",
                          password = "pass1234",
                          roles = ROLES.SPONSOR)

        #resemble someone using the edit_sponsor route in order to update the email associated with the sponsor we just created in MongoDB
        res = self.client.put("/api/sponsors/Bose/",
                              data = json.dumps({
                                  "email" : "boseofficial@gmail.com"
                              }),
                              content_type = "application/json")

        #ensure that the result indicates a success
        self.assertEqual(res.status_code, 201)

        #attempt to find the sponsor that we just updated
        updated_sponsor = Sponsor.findOne(sponsor_name = "Bose")

        #ensure that the sponsor was actually updated
        self.assertEqual(updated_sponsor.email, "boseofficial@gmail.com")  

    def test_edit_sponsor_invalid_json(self):
        
        #create a new sponsor document in MongoDB
        Sponsor.createOne(sponsor_name = "Hulu",
                          logo = "https://blob.knighthacks.org/somelogo.png",
                          subscription_tier = "Silver",
                          email = "hulu@gmail.com",
                          username = "huluofficial",
                          password = "pass1234",
                          roles = ROLES.SPONSOR)

        #resemble someone using the edit_sponsor route to update the sponsor with an empty json file
        res = self.client.put("/api/sponsors/Hulu/",
                              data = json.dumps({}),
                              content_type = "application/json")
        
        #ensure that the json file was invalid
        self.assertEqual(res.status_code, 400)
        
    def test_edit_sponsor_invalid_datatype(self):
        
        #create a new sponsor document in MongoDB
        Sponsor.createOne(sponsor_name = "Blu",
                          logo = "https://blob.knighthacks.org/somelogo.png",
                          subscription_tier = "Silver",
                          email = "blu@gmail.com",
                          username = "bluofficial",
                          password = "pass1234",
                          roles = ROLES.SPONSOR)

        #resemble someone using the edit sposonor route to update the email with an invalid datatype
        res = self.client.put("/api/sponsors/Blu/",
                              data = json.dumps({
                                  "email" : 123
                              }),
                              content_type = "application/json")
        
        #ensure that an invalid datatype was used to update the sponsor's email
        self.assertEqual(res.status_code, 400)

    def test_edit_sponsor_not_found(self):
        
        #create a new sponsor document in MongoDB
        Sponsor.createOne(sponsor_name = "Walmart",
                          logo = "https://blob.knighthacks.org/somelogo.png",
                          subscription_tier = "Gold",
                          email = "walmart@gmail.com",
                          username = "walmartofficial",
                          password = "pass1234",
                          roles = ROLES.SPONSOR)

        #resemble someone using the edit_sponsor route but they used the wrong sponsor name
        res = self.client.put("/api/sponsors/Walmarts/",
                              data = json.dumps({
                                  "email" : "walmartofficial@gmail.com"
                              }),
                              content_type = "application/json")

        #ensure that the sponsor was not found due to an incorrect name
        self.assertEqual(res.status_code, 404)

    def test_edit_sponsor_not_unique(self):
        
        #create a new sponsor document in MongoDB
        Sponsor.createOne(sponsor_name = "WellsFargo",
                          logo = "https://blob.knighthacks.org/somelogo.png",
                          subscription_tier = "Gold",
                          email = "wellsfargo@gmail.com",
                          username = "wellsfargoofficial",
                          password = "pass1234",
                          roles = ROLES.SPONSOR)

        #create a another, new sponsor document in MongoDB
        Sponsor.createOne(sponsor_name = "Walmart",
                          logo = "https://blob.knighthacks.org/somelogo.png",
                          subscription_tier = "Gold",
                          email = "walmart@gmail.com",
                          username = "walmartofficial",
                          password = "pass1234",
                          roles = ROLES.SPONSOR)

        #resemble someone using the edit_sponsor route but they used a non-unique username
        res = self.client.put("/api/sponsors/WellsFargo/",
                              data = json.dumps({
                                  "username" : "walmartofficial"
                              }),
                              content_type = "application/json")

        #ensure that the sponsor username was not unique
        self.assertEqual(res.status_code, 409)
