class TableMapping:
    def __init__(self, name: str, query: str, source_tables: list, primary_key: list = None):
        self.name = name
        self.query = query
        self.primary_key = primary_key
        self.source_tables = source_tables


views = {
    TableMapping("tags", """
        CREATE VIEW tags AS
        SELECT
            name AS name,
            count AS count
        FROM
            tags_raw;
    """, ["tags_raw"], ["name", "count"], ),

    TableMapping("users", """
        CREATE VIEW users AS
        SELECT
            id AS id,
            name AS name,
            email AS email,
            url AS url,
            deleted AS deleted,
            created_at AS created_at,
            updated_at AS updated_at,
            time_zone AS time_zone,
            phone AS phone,
            locale_id AS locale_id,
            locale AS locale,
            organization_id AS organizations_pk,
            role AS role,
            verified AS verified,
            external_id AS external_id,
            alias AS alias,
            active AS active,
            shared AS shared,
            shared_agent AS shared_agent,
            last_login_at AS last_login_at,
            two_factor_auth_enabled AS two_factor_auth_enabled,
            signature AS signature,
            details AS details,
            notes AS notes,
            custom_role_id AS custom_role_id,
            moderator AS moderator,
            ticket_restriction AS ticket_restriction,
            only_private_comments AS only_private_comments,
            restricted_agent AS restricted_agent,
            suspended AS suspended,
            chat_only AS chat_only,
            tags AS tags
        FROM
            users_raw;
    """, ["users_raw"], ["id"]),

    TableMapping("users_photos", """
        CREATE VIEW users_photos AS
        SELECT
            id AS users_pk,
            json(photo).id AS id,
            json(photo).file_name AS file_name,
            json(photo).content_url AS content_url,
            json(photo).content_type AS content_type,
            json(photo).size AS size,
            json(photo).width AS width,
            json(photo).height AS height,
            json(photo).inline AS inline
        FROM
            users_raw;
    """, ["users_raw"], ["id"]),

    TableMapping("users_groups", """
        CREATE VIEW users_groups AS
        SELECT
            user_id AS users_pk,
            group_id AS groups_pk,
            "default" AS "default",
            created_at AS created_at,
            updated_at AS updated_at
        FROM
            group_memberships_raw;
    """, ["group_memberships_raw"], ["users_pk", "groups_pk"]),

    TableMapping("groups", """
        CREATE VIEW groups AS
        SELECT
            id AS id,
            name AS name,
            url AS url,
            deleted AS deleted,
            created_at AS created_at,
            updated_at AS updated_at
        FROM
            groups_raw;
    """, ["groups_raw"], ["id"]),

    TableMapping("organizations", """
        CREATE VIEW organizations AS
        SELECT
            id AS id,
            name AS name,
            url AS url,
            shared_tickets AS shared_tickets,
            shared_comments AS shared_comments,
            external_id AS external_id,
            created_at AS created_at,
            updated_at AS updated_at,
            details AS details,
            notes AS notes,
            group_id AS groups_pk,
            tags AS tags
        FROM
            organizations_raw;
    """, ["organizations_raw"], ["id"]),

    TableMapping("organizations_domain_names", """
        CREATE VIEW organizations_domain_names AS
        SELECT
            id AS organizations_pk,
            unnest(from_json(domain_names,'["JSON"]')) AS "domain"
        FROM
            organizations_raw;
    """, ["organizations_raw"], ["organizations_pk", "domain"]),

    TableMapping("tickets", """
        CREATE VIEW tickets AS
        SELECT
            id AS id,
            url AS url,
            external_id AS external_id,
            type AS type,
            subject AS subject,
            priority AS priority,
            status AS status,
            recipient AS recipient,
            requester_id AS requester_users_pk,
            submitter_id AS submitter_users_pk,
            assignee_id AS assignee_users_pk,
            organization_id AS organizations_pk,
            group_id AS groups_pk,
            forum_topic_id AS topic_id,
            problem_id AS problem_id,
            has_incidents AS has_incidents,
            due_at AS due_at,
            json(via).channel AS via_channel,
            ticket_form_id AS ticket_form_id,
            brand_id AS brand_pk,
            created_at AS created_at,
            updated_at AS updated_at,
            tags AS tags
        FROM
            tickets_raw;
    """, ["tickets_raw"], ["id"]),

    TableMapping("tickets_fields_values", """
        CREATE VIEW tickets_fields_values AS
        SELECT
            id AS tickets_pk,
            json(custom_fields).value AS value,
            json(custom_fields).id AS tickets_fields_pk
        FROM
            tickets_raw;
    """, ["tickets_raw"], ["tickets_fields_pk", "tickets_pk"]),

    TableMapping("tickets_ratings", """
        CREATE VIEW tickets_ratings AS
        SELECT
            id AS tickets_pk,
            json(satisfaction_rating).score AS score,
            json(satisfaction_rating).id AS id,
        FROM
            tickets_raw;
    """, ["tickets_raw"], ["tickets_pk"]),

    TableMapping("tickets_metrics", """
        CREATE VIEW tickets_metrics AS
        SELECT
            id AS tickets_pk,
            json(metric_set).id AS id,
            json(metric_set).created_at AS created_at,
            json(metric_set).updated_at AS updated_at,
            json(metric_set).group_stations AS group_stations,
            json(metric_set).assignee_stations AS assignee_stations,
            json(metric_set).reopens AS reopens,
            json(metric_set).replies AS replies,
            json(metric_set).assignee_updated_at AS assignee_updated_at,
            json(metric_set).requester_updated_at AS requester_updated_at,
            json(metric_set).status_updated_at AS status_updated_at,
            json(metric_set).initially_assigned_at AS initially_assigned_at,
            json(metric_set).assigned_at AS assigned_at,
            json(metric_set).solved_at AS solved_at,
            json(metric_set).latest_comment_added_at AS latest_comment_added_at,
            json(metric_set).reply_time_in_minutes_calendar AS reply_time_in_minutes_calendar,
            json(metric_set).reply_time_in_minutes_business AS reply_time_in_minutes_business,
            json(metric_set).first_resolution_time_in_minutes.calendar AS first_resolution_time_in_minutes_calendar,
            json(metric_set).first_resolution_time_in_minutes.business AS first_resolution_time_in_minutes_business,
            json(metric_set).full_resolution_time_in_minutes.calendar AS full_resolution_time_in_minutes_calendar,
            json(metric_set).full_resolution_time_in_minutes.business AS full_resolution_time_in_minutes_business,
            json(metric_set).agent_wait_time_in_minutes.calendar AS agent_wait_time_in_minutes_calendar,
            json(metric_set).agent_wait_time_in_minutes.business AS agent_wait_time_in_minutes_business,
            json(metric_set).requester_wait_time_in_minutes.calendar AS requester_wait_time_in_minutes_calendar,
            json(metric_set).requester_wait_time_in_minutes.business AS requester_wait_time_in_minutes_business,
            json(metric_set).on_hold_time_in_minutes.calendar AS on_hold_time_in_minutes_calendar,
            json(metric_set).on_hold_time_in_minutes.business AS on_hold_time_in_minutes_business
        FROM
            tickets_raw;
    """, ["tickets_raw"], ["tickets_pk", "id"]),

    TableMapping("tickets_fields", """
    CREATE VIEW tickets_fields AS
    SELECT
        id AS id,
        type AS type,
        title AS title,
        active AS active,
        tag AS tag
    FROM
        ticket_fields_raw;
""", ["ticket_fields_raw"], ["id"]),

    TableMapping("tickets_comments", """
        CREATE VIEW tickets_comments AS
        SELECT
            id AS id,
            type AS type,
            body AS body,
            "public" AS "public",
            author_id AS author_pk,
            audit_id AS tickets_audits_pk,
            json(via).channel AS via_channel,
            json(metadata).system.ip_address AS ip_address,
            created_at AS created_at,
            ticket_id AS tickets_pk
        FROM
            ticket_comments_raw;
    """, ["ticket_comments_raw"], ["id"]),

    TableMapping("tickets_comments_attachments", """
        CREATE VIEW tickets_comments_attachments AS
        SELECT
            id AS tickets_comments_pk,
            json(attachments).id AS id,
            json(attachments).file_name AS file_name,
            json(attachments).content_url AS content_url,
            json(attachments).content_type AS content_type,
            json(attachments).size AS size,
            json(attachments).width AS width,
            json(attachments).height AS height,
            json(attachments).inline AS inline
        FROM
            ticket_comments_raw;
    """, ["ticket_comments_raw"], ["id"]),

    TableMapping("tickets_comments_attachments_thumbnails", """
        CREATE VIEW tickets_comments_attachments_thumbnails AS
        SELECT
            id AS tickets_comments_attachments_pk,
            json(attachments).thumbnails.id AS id,
            json(attachments).thumbnails.file_name AS file_name,
            json(attachments).thumbnails.content_url AS content_url,
            json(attachments).thumbnails.content_type AS content_type,
            json(attachments).thumbnails.size AS size,
            json(attachments).thumbnails.width AS width,
            json(attachments).thumbnails.height AS height,
            json(attachments).thumbnails.inline AS inline
        FROM
            ticket_comments_raw;
    """, ["ticket_comments_raw"], ["id"]),

    TableMapping("tickets_audits", """
        CREATE VIEW tickets_audits AS
        SELECT
            id AS id,
            ticket_id AS tickets_pk,
            created_at AS created_at,
            author_id AS author_pk,
            json(via).channel AS via_channel
        FROM
            ticket_audits_raw;
    """, ["ticket_audits_raw"], ["id"])
}
