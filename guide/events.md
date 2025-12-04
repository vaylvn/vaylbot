# Events

Vayl listens for a variety of events, allowing users to define actions that execute when these events occur. This document outlines all available events and the tags users can utilize to fetch event-specific information. All events are configured through their corresponding `.yml` files located in the `configuration/events` folder.

---

## Events and Tags

### Events Without Tags

These events do not provide any tags but allow for actions to be configured:
- **AD Break**
- **Vayl Load**
- **Stream Online**
- **Stream Offline**

### Events With Tags

#### **Chat**
- **Tags Available**:
  - `user`: The username of the user sending the message.
  - `message`: The content of the chat message.

#### **First Time Chat**
- **Tags Available**:
  - `user`: The username of the user sending their first-ever message in chat.
  - `message`: The content of the chat message.

#### **First Session Chat**
- **Tags Available**:
  - `user`: The username of the user sending their first message of the stream session.
  - `message`: The content of the chat message.

#### **Follow**
- **Tags Available**:
  - `user`: The username of the user who followed.

#### **Sub**
- **Tags Available**:
  - `user`: The username of the subscriber.
  - `total-months`: The total number of months the user has been subscribed.
  - `tier`: The subscription tier (e.g., `1`, `2`, `3`, `prime`).
  - `message`: The subscription message (if any).

#### **Gift Sub**
- **Tags Available**:
  - `user`: The username of the user gifting the subs.
  - `amount`: The number of subs gifted.
  - `tier`: The subscription tier of the gifted subs.

#### **Bits**
- **Tags Available**:
  - `user`: The username of the user who sent bits.
  - `amount`: The number of bits sent.
  - `message`: The message accompanying the bits (if any).

#### **Hype Train**
- **Tags Available**:
  - `level`: The current level of the Hype Train.
  - `conductor:bits`: The highest contributor to the Hype Train for bits.
  - `conductor:subs`: The highest contributor to the Hype Train for subs.
  - `level`: The current level of the Hype Train.

#### **Poll Create**
- **Tags Available**:
  - `title`: The title of the poll.
  - `option1`, `option2`, `option3`, etc.: The poll options (variable number depending on the poll).

#### **Poll Ended**
- **Tags Available**:
  - `title`: The title of the poll.
  - `option1bits`, `option2bits`, etc.: The amount of bits spent on each option.
  - `option1points`, `option2points`, etc.: The amount of channel points spent on each option.
  - `option1votes`, `option2votes`, etc.: The number of votes on each option.

#### **Prediction Create**
- **Tags Available**:
  - `title`: The title of the prediction.
  - `option1`, `option2`, `option3`, etc.: The prediction options (variable number).

#### **Prediction Locked**
- **Tags Available**:
  - `title`: The title of the prediction.
  - `option1`, `option2`, `option3`, etc.: The prediction options.
  - `option1points`, `option2points`, `option3points`, etc.: The amount of channel points spent on each option.

#### **Prediction Ended**
- **Tags Available**:
  - `title`: The title of the prediction.
  - `option1`, `option2`, `option3`, etc.: The prediction options.
  - `option1points`, `option2points`, `option3points`, etc.: The amount of channel points spent on each option.
  - `winner`: The winning option once the prediction is completed.

#### **Raid**
- **Tags Available**:
  - `user`: The username of the user initiating the raid.
  - `viewercount`: The number of viewers in the raid.

#### **Shoutout Given**
- **Tags Available**:
  - `user`: The username of the user receiving the shoutout.
  - `viewers`: The number of viewers in the recipient's stream.

#### **Shoutout Received**
- **Tags Available**:
  - `user`: The username of the user giving the shoutout.
  - `viewers`: The number of viewers in the shoutout giver's stream.

---

## Example Event Configuration

Below is an example of how to define actions for a specific event in its corresponding YAML file:

### Example: **Follow Event** `(configuration/events/follow.yml)`
```yaml
enabled: true
buffer: 0
actions:
- chat ; Thank you [user] for following!
- playsound ; follow_alert
```

In this example:
- When a **Follow** event occurs, Vayl will:
  - Send a chat message thanking the user by their username.
  - Play a sound alert.

---

## Best Practices

- **Use Tags Efficiently**: Incorporate tags to personalize responses or trigger dynamic actions.
- **Test Configurations**: Ensure your YAML files are correctly formatted and actions are tested before going live.
- **Combine Events with Actions**: Use events to enhance viewer interaction by pairing them with creative actions, such as OBS integrations or custom commands.

---

By leveraging events and their tags, you can create a fully customized and engaging Twitch chatbot experience with Vayl.
