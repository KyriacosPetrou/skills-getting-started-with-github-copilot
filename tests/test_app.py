def test_root_redirect(client):
    """Test root endpoint redirects to static index"""
    # Arrange: No special setup needed

    # Act: Make GET request to root
    response = client.get("/")

    # Assert: Should redirect to /static/index.html
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """Test getting all activities"""
    # Arrange: Activities are reset to initial state

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Should return 200 and the activities dict
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Check structure of one activity
    chess = data["Chess Club"]
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)


def test_signup_success(client):
    """Test successful signup for an activity"""
    # Arrange: Use an activity and email not already signed up
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 200 and success message
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]

    # Verify participant was added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity_name]["participants"]


def test_signup_duplicate(client):
    """Test signup when student is already signed up"""
    # Arrange: Use an activity and email already signed up
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 400 with error message
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_activity_not_found(client):
    """Test signup for non-existent activity"""
    # Arrange: Use invalid activity name
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 404 with error message
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_success(client):
    """Test successful unregister from an activity"""
    # Arrange: Use an activity and email already signed up
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert: Should return 200 and success message
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]

    # Verify participant was removed
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email not in activities_data[activity_name]["participants"]


def test_unregister_not_signed_up(client):
    """Test unregister when student is not signed up"""
    # Arrange: Use an activity and email not signed up
    activity_name = "Chess Club"
    email = "notsignedup@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert: Should return 400 with error message
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]


def test_unregister_activity_not_found(client):
    """Test unregister from non-existent activity"""
    # Arrange: Use invalid activity name
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert: Should return 404 with error message
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]