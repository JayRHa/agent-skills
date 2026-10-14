---
name: people-data
description: Research professional profiles and public business contact data through LinkedIn and YouTube, including profile details, email, phone, and channel business email lookup. Use when a user asks to identify, enrich, or find people, creators, or business contacts.
license: MIT
---

# People Data

Perform authorized people and public business-contact research through the Agent Body REST API.

Read [references/tool-reference.md](references/tool-reference.md) for exact endpoints, input fields, and auth.

## When to Use

- Look up a public professional profile from a canonical LinkedIn URL.
- Find a public business email or phone number tied to one profile.
- Find public business emails from YouTube channels.

## Workflow

1. Select the smallest endpoint that satisfies the request.
2. Prefer a canonical profile or channel URL. Do not invent a name-only search endpoint; request a canonical URL if none is available.
3. Use only documented `snake_case` query parameters.
4. Verify that returned identities match the request. Deduplicate search results by canonical profile identity when possible.
5. Present only returned contact data. Never construct or guess an email address or phone number.

## Examples

- Input: `Find the profile for https://www.linkedin.com/in/example-person/`
  Output: call `GET /v1/linkedin/profile?profile_url=https://www.linkedin.com/in/example-person/` and summarize only the returned public fields.
- Input: `Get the email for https://www.linkedin.com/in/example-person/`
  Output: call `GET /v1/linkedin/email?profile_url=https://www.linkedin.com/in/example-person/` if the endpoint finds one; otherwise say no result was returned.
- Input: `Find public business emails for https://www.youtube.com/@examplechannel`
  Output: call `GET /v1/youtube/channel/email?channel=https://www.youtube.com/@examplechannel` and preserve per-channel found/not-found status.

## Safety

Use contact information only for an authorized business purpose. Do not infer sensitive traits, bypass access controls, expose credentials, or treat a missing result as evidence that a person has no contact information.

## Best Practices

Use an existing user-provided Agent Body credential through a secure environment variable; never embed it in a skill, URL, output or log. Confirm the external provider is configured before sending profile URLs. Return the source URL and distinguish returned data from inference.

## Common Pitfalls

The upstream reference does not define a people-search route or filters. Do not promise that capability without a verified contract. API availability and paid access are provider-dependent; bundled examples are request shapes, not proof of a successful live lookup.

## Source

Adapted from [Agent Body people-data](https://github.com/Jess-yaozu/skills/tree/1a89674f1f9779f9d78ab418c43203a93a21663a/skills/people-data). Upstream MIT notice is retained in [LICENSE](LICENSE). The external API has not been called during this integration.
