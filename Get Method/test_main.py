from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_blogs():
    response = client.get("/blogs/all")
    assert response.status_code == 200 # Check for successful response, we assume we will get that response

def test_auth_error():
    response = client.post("/token", 
                data={})
    access_token = response.json().get("access_token")
    assert access_token == None
    #i want to check tht i get error message
    message = response.json().get("detail")[0].get("msg")
    assert message == "Field required" #this is the error message of your api. if not suree, put empty string ""

    response = client.post("/token", 
                data={"username":"", "password":""})
    access_token = response.json().get("access_token")
    assert access_token == None
    #i want to check tht i get error message
    message = response.json().get("detail")
    assert message == "Invalid Credentials"

def test_auth_success():
    response = client.post("/token", 
                data={"username":"cucu", "password":"cucu"})
    access_token = response.json().get("access_token")
    assert access_token

def test_post_article():
    auth = client.post("/token", 
                data={"username":"cucu", "password":"cucu"})
    access_token = auth.json().get("access_token")
    assert access_token
    response = client.post(
        "/article/",
        json={
            "title": "Test Article",
            "content": "This is a test article.",
            "published": True,
            "creator_id": 1
        },
        headers={"Authorization": "bearer " + access_token}
    )
    assert response.status_code == 200