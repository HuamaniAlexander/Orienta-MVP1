from app.domain.orientation.affinity import affinity


class BaselineEngine:
    version = "afinidad-1"

    def evaluate(self, responses, profile):
        return affinity(responses, profile)
