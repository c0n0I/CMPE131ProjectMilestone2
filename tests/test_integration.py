from app.models import Course, Assignment

def test_student_creates_folder_flow(client):
    client.post("/auth/login", data={"username": "testuser"}, follow_redirects=True)

    response = client.post(
        "/folders/add",
        data={"name": "Integration Folder"},
        follow_redirects=True
    )

    assert b"Integration Folder" in response.data

def test_student_creates_bookmark_flow(client):
    client.post("/auth/login", data={"username": "testuser"}, follow_redirects=True)

    response = client.post(
        "/bookmarks/add",
        data={
            "title": "Integration Bookmark",
            "url": "https://example.com"
        },
        follow_redirects=True
    )

    assert b"Integration Bookmark" in response.data

def test_instructor_course_assignment_flow(client):
    client.post("/auth/login", data={"username": "instructor"}, follow_redirects=True)

    response = client.post(
        "/courses/new",
        data={
            "title": "Integration Course",
            "description": "Course Desc"
        },
        follow_redirects=True
    )

    assert b"Integration Course" in response.data

    course = Course.query.filter_by(title="Integration Course").first()

    response = client.post(
        f"/courses/{course.id}/assignments/new",
        data={
            "title": "Integration Assignment",
            "description": "HW Desc"
        },
        follow_redirects=True
    )

    assert b"Integration Assignment" in response.data
