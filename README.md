# Zendesk Extractor

Zendesk is a customer service platform that helps businesses manage customer interactions across multiple channels. This component enables you to extract your Zendesk data into Keboola for analysis and reporting.

## Overview

This component enables you to extract various types of data from your Zendesk instance, including tickets, users, organizations, and custom fields. It supports both full and incremental data loading.

## Features

- Extracts data from multiple Zendesk endpoints
- Supports incremental loading for most tables
- Handles authentication via API token
- Provides detailed logging and debugging options
- Supports extraction of ticket details (comments and audits)

## Prerequisites

- Zendesk account with API access
- [API token](https://support.zendesk.com/hc/en-us/articles/4408889192858-Generating-a-new-API-token)

## Supported Endpoints

- `/api/v2/users.json`
- `/api/v2/groups.json`
- `/api/v2/group_memberships.json`
- `/api/v2/organizations.json`
- `/api/v2/tags.json`
- `/api/v2/ticket_fields.json`
- `/api/v2/incremental/tickets.json`
- `/api/v2/tickets/{ticket['id']}/comments.json`
- `/api/v2/tickets/{ticket['id']}/audits.json`

> Need more endpoints? Submit your request to [ideas.keboola.com](https://ideas.keboola.com/)

### Configuration

#### Authentication
```json
{
    "email": "your@email.com",
    "#api_token": "your_api_token",
    "sub_domain": "your_subdomain"
}
```

#### Sync Options
- **Full Sync**: Downloads all data from the source every run
- **Incremental Sync**: Downloads data (tickets, ticket_comments, ticket_audits) based on the `start_time` parameter. The start time is taken from the last successful run.

#### Destination
- **Full Load**: Destination table is overwritten every run
- **Incremental Load**: Data is upserted into the destination table. Tables with primary keys will have rows updated, tables without primary keys will have rows appended.

#### Available Details
- Comments
- Audits

> Note: Loading details has an impact on performance as they are loaded per ticket.

#### Debug
Enable detailed logging for troubleshooting purposes.

## Limitations

- API rate limits apply (see [Zendesk API documentation](https://developer.zendesk.com/api-reference/))

## Development

### Local Setup
1. Clone the repository:
```bash
git clone git@github.com:keboola/component-zendesk.git keboola.ex-zendesk-v2
cd keboola.ex-zendesk-v2
```

2. Configure local data folder in `docker-compose.yml`:
```yaml
volumes:
  - ./:/code
  - ./CUSTOM_FOLDER:/data
```

3. Build and run:
```bash
docker-compose build
docker-compose run --rm dev
```

### Testing
Run the test suite and lint check:
```bash
docker-compose run --rm test
```

## Integration

For deployment and integration with KBC, refer to the [deployment documentation](https://developers.keboola.com/extend/component/deployment/).

## Resources

- [Zendesk API Documentation](https://developer.zendesk.com/api-reference)
- [Keboola Documentation](https://help.keboola.com/)
- [Component Support](https://support.keboola.com/)
