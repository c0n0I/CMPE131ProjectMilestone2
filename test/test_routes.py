from app.models import User, Folder, Bookmark, db

def login(client, username="testuser"):
    return client.post("/auth/login", data={"username": username}, follow_redirects=True)


def test_login_route(client):
    response = login(client)
    assert b"Welcome" in response.data or b"Bookmarks" in response.data


def test_protected_bookmarks_requires_login(client):
    response = client.get("/bookmarks", follow_redirects=True)
    # Should redirect to login page
    assert b"Login" in response.data


def test_create_folder_route(client):
    login(client)
    response = client.post("/folders/add", data={"name": "New Folder"}, follow_redirects=True)

    assert b"Folder" in response.data
    assert Folder.query.filter_by(name="New Folder").first() is not None


def test_add_bookmark_with_folder(client):
    login(client)

    folder = Folder(name="My Folder", user_id=1)
    db.session.add(folder)
    db.session.commit()

    response = client.post(
        "/bookmarks/add",
        data={
            "title": "Google",
            "url": "https://google.com",
            "folder_id": folder.id
        },
        follow_redirects=True
    )

    assert b"Google" in response.data
    assert Bookmark.query.filter_by(title="Google").first().folder_id == folder.id
