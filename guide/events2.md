# Twitch Event Reference

Each supported event has a corresponding configuration file inside:

```
configuration/event/
```

These `.yml` files let you:
- Enable or disable the event (`enabled: true/false`)
- Define its queue behavior (`queue: front/back/instant`)
- Assign a list of actions to execute when triggered

Example configuration:
```yaml
enabled: true
queue: front
actions:
- chat | Hello, [user_name]!
```

### Queue Behavior
| Value | Description |
|--------|--------------|
| **front** | Places the event at the front of the queue, but still waits for any currently playing alert to finish. |
| **back** | Places the event at the back of the queue. |
| **instant** | Triggers immediately, bypassing the queue. |

All events expose a set of tags (e.g. `[user_name]`, `[broadcaster_user_name]`, `[title]`) that can be used inside your actions.

> **Note:** The **Redeem** (Reward Add) event has its own dedicated configuration page — see [redeems.md](redeems.md).

---

## Supported Events

<details><summary><strong>Ad Break Begin</strong> — Triggered when an ad break starts.</summary>

| Tag | Description |
|------|-------------|
| [duration_seconds] | Length of the ad break in seconds. |
| [started_at] | Time the ad break started. |
| [is_automatic] | Whether the ad break was automatically triggered. |
| [broadcaster_user_id] | ID of the broadcaster. |
| [broadcaster_user_login] | Login name of the broadcaster. |
| [broadcaster_user_name] | Display name of the broadcaster. |
| [requester_user_id] | ID of the requester. |
| [requester_user_login] | Login name of the requester. |
| [requester_user_name] | Display name of the requester. |

</details>

<details><summary><strong>Cheer</strong> — Triggered when a user sends bits in chat.</summary>

| Tag | Description |
|------|-------------|
| [is_anonymous] | Whether the cheer was sent anonymously. |
| [user_id] | ID of the cheering user. |
| [user_login] | Login name of the cheering user. |
| [user_name] | Display name of the cheering user. |
| [broadcaster_user_id] | ID of the broadcaster. |
| [broadcaster_user_login] | Login name of the broadcaster. |
| [broadcaster_user_name] | Display name of the broadcaster. |
| [message] | Message attached to the cheer. |
| [bits] | Number of bits cheered. |

</details>

<details><summary><strong>Follow</strong> — Triggered when a user follows the broadcaster.</summary>

| Tag | Description |
|------|-------------|
| [user_id] | ID of the follower. |
| [user_login] | Login name of the follower. |
| [user_name] | Display name of the follower. |
| [broadcaster_user_id] | ID of the broadcaster. |
| [broadcaster_user_login] | Login name of the broadcaster. |
| [broadcaster_user_name] | Display name of the broadcaster. |
| [followed_at] | Time the follow occurred. |

</details>

<details><summary><strong>Hype Train Begin</strong> — Triggered when a new Hype Train starts.</summary>

| Tag | Description |
|------|-------------|
| [id] | Hype train ID. |
| [broadcaster_user_id] | ID of the broadcaster. |
| [broadcaster_user_login] | Login name of the broadcaster. |
| [broadcaster_user_name] | Display name of the broadcaster. |
| [total] | Total contributions to the hype train. |
| [progress] | Current progress value. |
| [goal] | Goal value required to complete this level. |
| [top_contributions.1.user_id] | ID of the top contributor. |
| [top_contributions.1.user_login] | Login name of the top contributor. |
| [top_contributions.1.user_name] | Display name of the top contributor. |
| [top_contributions.1.type] | Type of contribution (bits, subscription). |
| [top_contributions.1.total] | Total contributed amount. |
| [last_contribution.user_id] | ID of the last contributor. |
| [last_contribution.user_login] | Login of the last contributor. |
| [last_contribution.user_name] | Display name of the last contributor. |
| [last_contribution.type] | Type of the last contribution. |
| [last_contribution.total] | Total of the last contribution. |
| [level] | Current hype train level. |
| [started_at] | When the hype train began. |
| [expires_at] | When the hype train ends. |
| [is_golden_kappa_train] | Whether this is a golden kappa train. |

</details>

<details><summary><strong>Poll Begin</strong> — Triggered when a new poll starts.</summary>

| Tag | Description |
|------|-------------|
| [id] | Poll ID. |
| [broadcaster_user_id] | Broadcaster ID. |
| [broadcaster_user_login] | Broadcaster login. |
| [broadcaster_user_name] | Broadcaster display name. |
| [title] | Poll title. |
| [choices.1.id] | ID of a poll choice. |
| [choices.1.title] | Title of the choice. |
| [bits_voting.is_enabled] | Whether bit voting is enabled. |
| [bits_voting.amount_per_vote] | Amount of bits required per vote. |
| [channel_points_voting.is_enabled] | Whether channel points voting is enabled. |
| [channel_points_voting.amount_per_vote] | Points required per vote. |
| [started_at] | Start time of the poll. |
| [ends_at] | End time of the poll. |

</details>

<details><summary><strong>Poll End</strong> — Triggered when a poll ends.</summary>

| Tag | Description |
|------|-------------|
| [id] | Poll ID. |
| [broadcaster_user_id] | Broadcaster ID. |
| [broadcaster_user_login] | Broadcaster login. |
| [broadcaster_user_name] | Broadcaster display name. |
| [title] | Poll title. |
| [choices.1.id] | ID of a poll choice. |
| [choices.1.title] | Title of the choice. |
| [choices.1.bits_votes] | Number of bits votes. |
| [choices.1.channel_points_votes] | Number of channel point votes. |
| [choices.1.votes] | Total votes. |
| [bits_voting.is_enabled] | Whether bit voting is enabled. |
| [bits_voting.amount_per_vote] | Bits required per vote. |
| [channel_points_voting.is_enabled] | Whether channel points voting is enabled. |
| [channel_points_voting.amount_per_vote] | Points required per vote. |
| [status] | Poll status. |
| [started_at] | Start time. |
| [ended_at] | End time. |

</details>

<details><summary><strong>Prediction Begin</strong> — Triggered when a new prediction begins.</summary>

| Tag | Description |
|------|-------------|
| [id] | Prediction ID. |
| [broadcaster_user_id] | Broadcaster ID. |
| [broadcaster_user_login] | Broadcaster login. |
| [broadcaster_user_name] | Broadcaster display name. |
| [title] | Prediction title. |
| [outcomes.1.id] | Outcome ID. |
| [outcomes.1.title] | Outcome title. |
| [outcomes.1.color] | Outcome color. |
| [started_at] | Start time. |
| [locks_at] | Lock time. |

</details>

<details><summary><strong>Prediction Lock</strong> — Triggered when prediction betting locks.</summary>

| Tag | Description |
|------|-------------|
| [id] | Prediction ID. |
| [broadcaster_user_id] | Broadcaster ID. |
| [broadcaster_user_login] | Broadcaster login. |
| [broadcaster_user_name] | Broadcaster display name. |
| [title] | Prediction title. |
| [outcomes.1.id] | Outcome ID. |
| [outcomes.1.title] | Outcome title. |
| [outcomes.1.color] | Outcome color. |
| [outcomes.1.users] | Total number of users who voted. |
| [outcomes.1.channel_points] | Total points spent. |
| [outcomes.1.top_predictors.1.user_name] | Name of top predictor. |
| [outcomes.1.top_predictors.1.user_login] | Login of top predictor. |
| [outcomes.1.top_predictors.1.user_id] | ID of top predictor. |
| [outcomes.1.top_predictors.1.channel_points_used] | Points used. |
| [started_at] | Start time. |
| [locked_at] | Locked time. |

</details>

<details><summary><strong>Prediction End</strong> — Triggered when prediction resolves.</summary>

| Tag | Description |
|------|-------------|
| [id] | Prediction ID. |
| [broadcaster_user_id] | Broadcaster ID. |
| [broadcaster_user_login] | Broadcaster login. |
| [broadcaster_user_name] | Broadcaster display name. |
| [title] | Prediction title. |
| [winning_outcome_id] | Winning outcome ID. |
| [outcomes.1.id] | Outcome ID. |
| [outcomes.1.title] | Outcome title. |
| [outcomes.1.color] | Outcome color. |
| [outcomes.1.users] | Users who participated. |
| [outcomes.1.channel_points] | Channel points total. |
| [outcomes.1.top_predictors.1.user_name] | Predictor username. |
| [outcomes.1.top_predictors.1.user_login] | Predictor login. |
| [outcomes.1.top_predictors.1.user_id] | Predictor ID. |
| [outcomes.1.top_predictors.1.channel_points_won] | Points won. |
| [outcomes.1.top_predictors.1.channel_points_used] | Points used. |
| [status] | Resolution status. |
| [started_at] | Start time. |
| [ended_at] | End time. |

</details>

<details><summary><strong>Redeem</strong> — Triggered when a channel point reward is redeemed.</summary>

See [redeems.md](redeems.md) for full configuration and tag details.

</details>

<details><summary><strong>Redeem Update</strong> — Triggered when a reward redemption is updated.</summary>

| Tag | Description |
|------|-------------|
| [id] | Redemption ID. |
| [broadcaster_user_id] | Broadcaster ID. |
| [broadcaster_user_login] | Broadcaster login. |
| [broadcaster_user_name] | Broadcaster display name. |
| [user_id] | Redeeming user ID. |
| [user_login] | Redeeming user login. |
| [user_name] | Redeeming user display name. |
| [user_input] | Custom user input. |
| [status] | Redemption status. |
| [reward.id] | Reward ID. |
| [reward.title] | Reward title. |
| [reward.cost] | Reward cost. |
| [reward.prompt] | Reward prompt. |
| [redeemed_at] | Redemption time. |

</details>

<details><summary><strong>Shoutout Create</strong> — Triggered when a shoutout is created.</summary>

| Tag | Description |
|------|-------------|
| [broadcaster_user_id] | Broadcaster ID. |
| [broadcaster_user_name] | Broadcaster display name. |
| [broadcaster_user_login] | Broadcaster login. |
| [moderator_user_id] | Moderator ID. |
| [moderator_user_name] | Moderator name. |
| [moderator_user_login] | Moderator login. |
| [to_broadcaster_user_id] | Target broadcaster ID. |
| [to_broadcaster_user_name] | Target broadcaster name. |
| [to_broadcaster_user_login] | Target broadcaster login. |
| [started_at] | Shoutout start time. |
| [viewer_count] | Viewer count. |
| [cooldown_ends_at] | Broadcaster cooldown end. |
| [target_cooldown_ends_at] | Target cooldown end. |

</details>

<details><summary><strong>Shoutout Receive</strong> — Triggered when a shoutout is received.</summary>

| Tag | Description |
|------|-------------|
| [broadcaster_user_id] | Receiving broadcaster ID. |
| [broadcaster_user_name] | Receiving broadcaster name. |
| [broadcaster_user_login] | Receiving broadcaster login. |
| [from_broadcaster_user_id] | Source broadcaster ID. |
| [from_broadcaster_user_name] | Source broadcaster name. |
| [from_broadcaster_user_login] | Source broadcaster login. |
| [viewer_count] | Viewer count. |
| [started_at] | Start time. |

</details>

<details><summary><strong>Stream Offline</strong> — Triggered when the stream ends.</summary>

| Tag | Description |
|------|-------------|
| [broadcaster_user_id] | Broadcaster ID. |
| [broadcaster_user_login] | Broadcaster login. |
| [broadcaster_user_name] | Broadcaster name. |

</details>

<details><summary><strong>Stream Online</strong> — Triggered when the stream goes live.</summary>

| Tag | Description |
|------|-------------|
| [id] | Stream ID. |
| [broadcaster_user_id] | Broadcaster ID. |
| [broadcaster_user_login] | Broadcaster login. |
| [broadcaster_user_name] | Broadcaster name. |
| [type] | Stream type. |
| [started_at] | Stream start time. |

</details>

<details><summary><strong>Subscription</strong> — Triggered when a user subscribes.</summary>

| Tag | Description |
|------|-------------|
| [user_id] | Subscriber ID. |
| [user_login] | Subscriber login. |
| [user_name] | Subscriber display name. |
| [broadcaster_user_id] | Broadcaster ID. |
| [broadcaster_user_login] | Broadcaster login. |
| [broadcaster_user_name] | Broadcaster name. |
| [tier] | Subscription tier. |
| [is_gift] | Whether the sub was a gift. |

</details>

<details><summary><strong>Subscription – GiftSub</strong> — Triggered when a user gifts subscriptions.</summary>

| Tag | Description |
|------|-------------|
| [user_id] | Gifter ID. |
| [user_login] | Gifter login. |
| [user_name] | Gifter display name. |
| [broadcaster_user_id] | Broadcaster ID. |
| [broadcaster_user_login] | Broadcaster login. |
| [broadcaster_user_name] | Broadcaster name. |
| [total] | Total gifted in this event. |
| [tier] | Gift tier. |
| [cumulative_total] | Cumulative gifted total. |
| [is_anonymous] | Whether the gift was anonymous. |

</details>

<details><summary><strong>Subscription – ReSub</strong> — Triggered when a subscriber shares a resub message.</summary>

| Tag | Description |
|------|-------------|
| [user_id] | Subscriber ID. |
| [user_login] | Subscriber login. |
| [user_name] | Subscriber display name. |
| [broadcaster_user_id] | Broadcaster ID. |
| [broadcaster_user_login] | Broadcaster login. |
| [broadcaster_user_name] | Broadcaster name. |
| [tier] | Subscription tier. |
| [message.text] | Message text. |
| [message.emotes.1.begin] | Emote start index. |
| [message.emotes.1.end] | Emote end index. |
| [message.emotes.1.id] | Emote ID. |
| [cumulative_months] | Total months subscribed. |
| [streak_months] | Consecutive months streak. |
| [duration_months] | Months purchased in this sub. |

</details>
