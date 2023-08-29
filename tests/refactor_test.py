class Query:
    def __init__(self, session):
        self.session = session

    def elements(self):
        return ElementsQuery(self.session)

class ElementsQuery:
    def __init__(self, session):
        self.session = session

    def all(self):
        # Perform logic to retrieve all elements using the session
        return ["element1", "element2", "element3"]  # Replace with actual data retrieval logic

class Session:
    def query(self):
        return Query(self)

session = Session()
result = session.query().elements().all()
print(result)