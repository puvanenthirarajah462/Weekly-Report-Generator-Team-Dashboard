from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper


def patch_mariadb_compatibility():
    if getattr(MySQLDatabaseWrapper, "_weekly_report_dashboard_patched", False):
        return

    original_get_database_version = MySQLDatabaseWrapper.get_database_version

    def get_database_version(self):
        version = original_get_database_version(self)
        if version and version[:2] == (10, 4):
            return (10, 5)
        return version

    MySQLDatabaseWrapper.get_database_version = get_database_version
    MySQLDatabaseWrapper._weekly_report_dashboard_patched = True
