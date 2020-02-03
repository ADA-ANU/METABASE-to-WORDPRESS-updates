# METABASE-to-WORDPRESS-updates

Code to update the ADA wordpress website (https://ada.edu.au) with newly published, and recently updated, datasets.

The metabase API is used to query results from the Dataverse postgres database for new and updated datasets.

The wordpress API is then used to write new posts to the ada website. The categories of these new posts are set such that the new posts are displayed in the correct section of the wordpress site.

The code also updates the ADA twitter feed to let twitter users know when there are new and updated ADA datasets.

