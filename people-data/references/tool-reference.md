# People Data API Reference

Base URL: `https://api.agentbody.io`. Every request requires `Authorization: Bearer <API_KEY>`.

| API | Required query field | Purpose |
|---|---|---|
| `GET /v1/linkedin/profile` | `profile_url` | Retrieve one professional profile |
| `GET /v1/linkedin/email` | `profile_url` | Look up public business email data |
| `GET /v1/linkedin/phone` | `profile_url` | Look up public business phone data |
| `GET /v1/youtube/channel/email` | `channel` | Find public business email for one channel |

## People search fields

`GET /v1/linkedin/profile` and the related lookup endpoints use the documented `snake_case` query fields from the live API contract.

The YouTube endpoint accepts optional `scrape_fresh_email`. Preserve returned found/not-found state instead of inventing missing addresses.
