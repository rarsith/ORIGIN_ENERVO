class DbStatuses(object):
    wip: str = "WIP"
    init: str = "INIT"
    in_progress: str = "IN PROGRESS"
    pending_rev: str = "PENDING-REVIEW"
    approved_internal: str = "APPROVED_INT"
    approved_client: str = "APPROVED_CLIENT"
    approved_temp: str = "APPROVED_TEMP"
    approved_tech: str = "APPROVED_TECH"