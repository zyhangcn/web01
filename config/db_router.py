class WEB_router():
    db_list = ['default', 'db1']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.db_list:
            return model._meta.app_label
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.db_list:
            return model._meta.app_label
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db in self.db_list:

            if app_label == "db1":
                return True

        return None
