class DbEntityBaseAttributes:
    _id: str
    show_name: str
    branch_name: str
    category: str
    entry_name: str
    entity_type: str
    status: str
    active: bool
    date: str
    time: str
    owner: str

    def __init__(self, _id, show_name, branch_name, category, entry_name, entity_type, status, active, date, time, owner):
        self.id = _id
        self.show_name = show_name
        self.branch_name = branch_name
        self.category = category
        self.entry_name = entry_name
        self.entity_type = entity_type
        self.status = status
        self.active = active
        self.date = date
        self.time = time
        self.owner = owner


