from locust import HttpUser, task, between

class CMSUser(HttpUser):
    wait_time = between(1, 5)  # wait time between tasks

    @task
    def get_home(self):
        self.client.get("/api/blogs/")  # Replace with your actual endpoint

    @task
    def create_blog(self):
        self.client.post("/api/blogs/create/", json={
            "title": "Test Post",
            "category": "Testing",
            "author": "Load Tester",
            "content": "This is a load test post."
        })
