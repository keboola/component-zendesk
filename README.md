keboola.ex-zendesk-v2
=============

Prerequisites
=============

[How to obtain API token](https://support.zendesk.com/hc/en-us/articles/4408889192858-Generating-a-new-API-token)

Supported endpoints
===================

    - /api/v2/users.json
    - /api/v2/groups.json
    - /api/v2/group_memberships.json
    - /api/v2/organizations.json
    - /api/v2/tags.json", Tags
    - /api/v2/ticket_fields.json
    - /api/v2/incremental/tickets.json
    - /api/v2/tickets/{ticket['id']}/comments.json
    - /api/v2/tickets/{ticket['id']}/audits.json

If you need more endpoints, please submit your request to
[ideas.keboola.com](https://ideas.keboola.com/)

Configuration
=============

### authentication
- email
- #api_token
- sub_domain

### sync options
- Full Sync downloads all data from the source every run
- Incremental Sync downloads data (tickets, ticket_comments and ticket_audits) by parameter start_time described <a href='https://developer.zendesk.com/api-reference/ticketing/ticket-management/incremental_exports/#per_page'>here</a>. The start time is taken from the last successful run. 

### destination
#### load type
- Full load is used, the destination table will be overwritten every run
- incremental load is used, data will be upserted into the destination table. Tables with a primary key will have rows updated, tables without a primary key will have rows appended.

### available details
#### Details of tickets which will be loaded also. Details are loaded per ticket. It has an impact on performance.
- Comments
- Audits

### debug
#### If checked, the component will output more detailed information about the run.

Output
======

List of output tables is described [here](https://help.keboola.com/components/extractors/communication/zendesk/)

Development
-----------

If required, change local data folder (the `CUSTOM_FOLDER` placeholder) path to
your custom path in the `docker-compose.yml` file:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    volumes:
      - ./:/code
      - ./CUSTOM_FOLDER:/data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone this repository, init the workspace and run the component with following
command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
git clone git@github.com:keboola/component-zendesk.git keboola.ex-zendesk-v2
cd keboola.ex-zendesk-v2
docker-compose build
docker-compose run --rm dev
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the test suite and lint check using this command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
docker-compose run --rm test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integration
===========

For information about deployment and integration with KBC, please refer to the
[deployment section of developers
documentation](https://developers.keboola.com/extend/component/deployment/)
