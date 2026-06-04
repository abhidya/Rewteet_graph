from server import app


def main():
    client = app.test_client()
    health = client.get("/health")
    assert health.status_code == 200
    response = client.post("/results", data={"input_text[]": ["alice", "bob", "carol"]})
    assert response.status_code == 200
    assert b"User,alice,bob,carol" in response.data


if __name__ == "__main__":
    main()
