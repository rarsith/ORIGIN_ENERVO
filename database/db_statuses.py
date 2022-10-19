class DbStatuses:
    wip: str = "WIP"
    init: str = "INIT"
    in_progress: str = "IN PROGRESS"
    pending_rev: str = "PENDING-REVIEW"
    tweak: str = "TWEAK"
    approved_internal: str = "APPROVED_INT"
    approved_client: str = "APPROVED_CLIENT"
    approved_temp: str = "APPROVED_TEMP"
    approved_tech: str = "APPROVED_TECH"

    def list_all(self):
        list_all_statuses = [self.wip,
                             self.init,
                             self.in_progress,
                             self.pending_rev,
                             self.tweak,
                             self.approved_internal,
                             self.approved_client,
                             self.approved_temp,
                             self.approved_tech]
        return list_all_statuses


if __name__ == "__main__":
    cc = DbStatuses()
    print (str(cc.list_all()))