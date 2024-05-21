import django.db.models.deletion
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import connection, migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtail_cfran", "0025_alter_contentpage_body"),
    ]

    def getSQLRenameContentManagerQuery(name_from, name_to):
        # "UPDATE django_content_type SET model='config' WHERE app_label='%s' and model='wagtailcfranconfig';" % (name_to + '')
        # "ALTER TABLE IF EXISTS '%s' RENAME TO '%s';" % (name_to + '_wagtailcfranconfig', name_to + '_config')
        # "ALTER SEQUENCE IF EXISTS '%s' RENAME TO '%s';" % (name_to + '_wagtailcfranconfig_id_seq', name_to + '_config_id_seq')
        sql_query = (
            "UPDATE django_content_type SET app_label='{}' WHERE app_label='{}';".format(name_to, name_from),
            "ALTER TABLE {}_analyticssettings RENAME TO {}_analyticssettings;".format(name_from, name_to),
            "ALTER TABLE {}_megamenucategory RENAME TO {}_megamenucategory;".format(name_from, name_to),
            "ALTER TABLE {}_megamenu RENAME TO {}_megamenu;".format(name_from, name_to),
            "ALTER TABLE {}_tagcontentpage RENAME TO {}_tagcontentpage;".format(name_from, name_to),
            "ALTER TABLE {}_socialmediaitem RENAME TO {}_socialmediaitem;".format(name_from, name_to),
            "ALTER TABLE {}_contentpage RENAME TO {}_contentpage;".format(name_from, name_to),
            "ALTER SEQUENCE {}_analyticssettings_id_seq RENAME TO {}_analyticssettings_id_seq;".format(
                name_from, name_to
            ),
            "ALTER SEQUENCE {}_megamenu_id_seq RENAME TO {}_megamenu_id_seq;".format(name_from, name_to),
            "ALTER SEQUENCE {}_megamenucategory_id_seq RENAME TO {}_megamenucategory_id_seq;".format(
                name_from, name_to
            ),
            "ALTER SEQUENCE {}_socialmediaitem_id_seq RENAME TO {}_socialmediaitem_id_seq;".format(name_from, name_to),
            "ALTER SEQUENCE {}_tagcontentpage_id_seq RENAME TO {}_tagcontentpage_id_seq;".format(name_from, name_to),
            "ALTER SEQUENCE IF EXISTS {}_contentpage_id_seq RENAME TO {}_contentpage_id_seq;".format(
                name_from, name_to
            ),
            "UPDATE django_migrations SET app='{}' WHERE app='{}';".format(name_to, name_from),
            "UPDATE django_migrations SET name = replace(name,'{}','{}') WHERE app ='{}';".format(
                name_from.replace("_", ""), name_to.replace("_", ""), name_to
            ),
        )
        return sql_query

    def getSQLRenameDSFRQuery(name_from, name_to):
        sql_query = (
            "UPDATE django_content_type SET app_label='{}' WHERE app_label='{}';".format(name_to, name_from),
            "ALTER TABLE IF EXISTS  {}_cmsdsfrconfig RENAME TO {}_{}config;".format(
                name_from, name_to, name_to.replace("_", "")
            ),
            "ALTER SEQUENCE IF EXISTS {}_cmsdsfrconfig_id_seq RENAME TO {}_{}config_id_seq;".format(
                name_from, name_to, name_to.replace("_", "")
            ),
            "ALTER TABLE IF EXISTS  {}_{}config RENAME TO {}_{}config;".format(
                name_from, name_from.replace("_", ""), name_to, name_to.replace("_", "")
            ),
            "ALTER SEQUENCE IF EXISTS {}_{}config_id_seq RENAME TO {}_{}config_id_seq;".format(
                name_from, name_from.replace("_", ""), name_to, name_to.replace("_", "")
            ),
            "ALTER TABLE IF EXISTS {}_dsfrconfig RENAME TO {}_dsfrconfig;".format(name_from, name_to),
            "ALTER TABLE IF EXISTS {}_dsfrsocialmedia RENAME TO {}_dsfrsocialmedia;".format(name_from, name_to),
            "ALTER SEQUENCE IF EXISTS  {}_dsfrconfig_id_seq RENAME TO {}_dsfrconfig_id_seq;".format(
                name_from, name_to
            ),
            "ALTER SEQUENCE IF EXISTS {}_dsfrsocialmedia_id_seq RENAME TO {}_dsfrsocialmedia_id_seq;".format(
                name_from, name_to
            ),
            "UPDATE django_migrations SET app='{}' WHERE app='{}';".format(name_to, name_from),
            "UPDATE django_migrations SET name = replace(name,'{}','{}') WHERE app ='{}';".format(
                name_from.replace("_", ""), name_to.replace("_", ""), name_to
            ),
        )
        return sql_query

    db_cursor = connection.cursor()
    db_cursor.execute("SELECT relname FROM pg_class WHERE relname='content_manager_contentpage';")
    result_content_manager = bool(db_cursor.fetchone())
    db_cursor.execute("SELECT relname FROM pg_class WHERE relname='wagtail_fastoche_contentpage';")
    result_wagtail_fastoche = bool(db_cursor.fetchone())
    if result_content_manager:
        sql_query = getSQLRenameContentManagerQuery("content_manager", "wagtail_cfran") + getSQLRenameDSFRQuery(
            "content_manager", "wagtail_cfran"
        )
        reverse_sql_query = getSQLRenameContentManagerQuery(
            "wagtail_cfran", "content_manager"
        ) + getSQLRenameDSFRQuery("wagtail_cfran", "content_manager")
        operations = [
            migrations.RunSQL(sql=sql_query, reverse_sql=reverse_sql_query),
        ]

    elif result_wagtail_fastoche:
        sql_query = getSQLRenameContentManagerQuery("wagtail_fastoche", "wagtail_cfran") + getSQLRenameDSFRQuery(
            "wagtail_fastoche", "wagtail_cfran"
        )
        reverse_sql_query = getSQLRenameContentManagerQuery(
            "wagtail_cfran", "wagtail_fastoche"
        ) + getSQLRenameDSFRQuery("wagtail_cfran", "wagtail_fastoche")
        operations = [
            migrations.RunSQL(sql=sql_query, reverse_sql=reverse_sql_query),
        ]
    else:
        operations = []
