Migrate old reports
===================

1. Before running migration scripts you should read ../README.txt in order
   to install and configure this package;

2. In config.py update REPORTS_XML with url that exports your old reports
   as XML and as this is a python file you'll have to restart zope;

3. In config.py update REPORTS_CONTAINER with the name of the folder you want
   old reports to be imported;

4. In your browser login into your plone portal as manager and go to
   plone site url and request @@migrate_reports script

   For example:

      http://<portal_url>:<port>/www/SITE/@@migrate_reports

   Note: This script looks for REPORTS_CONTAINER you set in step 3 in
   context and if it doesn't exists, it will create it. So if you go to

      http://<portal_url>:<port>/www/SITE

   and

      REPORTS_CONTAINER = 'publications'

   your English reports will be imported to:

      http://<portal_url>:<port>/www/SITE/publications

5. After all reports are imported, run @@migrate_relations script.

   For example:

      http://<portal_url>:<port>/www/SITE/@@migrate_relations

6. Go to administration section > vocabularies and update publications_groups
   items as these were generated automatically at migration time.
