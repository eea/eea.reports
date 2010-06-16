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

   Note: As there are to many reports to import is indicated to import them in
   more than one step, for that you can specify year like:

      http://<portal_url>:<port>/www/SITE/@@migrate_reports?year=2008

   For reports that doesn't have year specified you can use 'year=-1'. Also
   as there are a lot of reports without year specified you can split results
   adding 'start'index and 'stop' index of reports list. For example:

      http://<portal_url>:<port>/www/SITE/@@migrate_reports?year=-1&start=0&stop=10

   These parameters works only if year is specified. You also can omit one of
   them, and the results will be everithing from that point, or everithing
   to that point. For example:

      http://<portal_url>:<port>/www/SITE/@@migrate_reports?year=2008&start=20

   Returns all reports from year 2008 without first 20.

      http://<portal_url>:<port>/www/SITE/@@migrate_reports?year=2008&stop=15

   Returns first 15 reports from year 2008.

5. After all reports are imported, run @@migrate_relations script.

   For example:

      http://<portal_url>:<port>/www/SITE/@@migrate_relations

6. After you run @@migrate_relations script, run @@migrate_serialtitle script.

   For example:

      http://<portal_url>:<port>/www/SITE/@@migrate_serialtitle

7. Go to administration section > vocabularies and update publications_groups
   items as these were generated automatically at migration time.

8. Run @@migrate_sortorder in order to fix additional files order.

   For example:

      http://<portal_url>:<port>/www/SITE/@@migrate_sortorder
