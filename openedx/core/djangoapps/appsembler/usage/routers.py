from __future__ import absolute_import, unicode_literals


class AppsemblerUsageRouter(object):
    """
    Database router to send usage aggregation to Cloud SQL
    """
    app_label = 'appsembler_usage'
    db_alias = 'appsembler_usage'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return self.db_alias

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return self.db_alias

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # this app shouldn't be on any other db
        # and this db shouldn't have any other apps
        if app_label == self.app_label:
            return db == self.db_alias
        elif db == self.db_alias:
            return False
