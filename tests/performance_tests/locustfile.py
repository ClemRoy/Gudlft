from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task
    def index(self):
        response = self.client.get("/")

    @task
    def login(self):
        response = self.client.post(
            "/showSummary", {"email": "john@simplylift.co"})

    @task
    def book_link(self):
        response = self.client.get("/book/Future%20comp/Simply%20Lift")

    @task
    def purchase_place(self):
        response = self.client.post(
            '/purchasePlaces', data={
                "competition": "Future comp",
                "club": "Simply Lift",
                "places": 5})

    @task
    def logout(self):
        response = self.client.get('/logout')
