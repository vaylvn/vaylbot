# **Default Commands**
Looking for [Custom Commands?](custom-commands.md)

Vayl Bot includes a set of default commands to simplify stream management and enhance viewer interaction. Below is a comprehensive list of the commands, categorized by their access levels and functionality.

---

## **Streamer and Moderator Commands**

### `!setgame`

- **Access**: Streamer and Moderators
- **Description**: Updates the stream's current game.
- **Example**:
  ```
  !setgame Minecraft
  ```

### `!settitle`

- **Access**: Streamer and Moderators
- **Description**: Updates the stream's title.
- **Example**:
  ```
  !settitle Building an Epic Base!
  ```

### \*\*3. \*\***`!addquote`**

- **Access**: Streamer and Moderators
- **Description**: Saves a chat message as a quote. Must be used as a reply to the message.

---

## **Streamer-Only Commands**

### `!debug`

`!debug` is a powerful command designed for streamers to simulate various events for testing purposes. It allows you to ensure that actions, triggers, and integrations work as expected.

#### **Usage**:

```bash
!debug <event_type> [arguments]
```

#### **Supported Event Types**:

1. **ad-break**: Simulates an ad break.


2. **vayl-load**: Simulates Vayl loading.


3. **stream-online**: Simulates the stream going online.


4. **stream-offline**: Simulates the stream going offline.


5. **hypetrain**: Simulates a hype train.

   - **Arguments**: `<level>` (e.g., 1, 2, etc.).
   - **Example**:
     ```
     !debug hypetrain 2
     ```

6. **first-time-chat**: Simulates a user’s first-ever chat.

   - **Arguments**: `<username>`.
   - **Example**:
     ```
     !debug first-time-chat NewUser
     ```

7. **first-session-chat**: Simulates a user’s first chat in the current session.

   - **Arguments**: `<username>`.
   - **Example**:
     ```
     !debug first-session-chat RegularUser
     ```

8. **follow**: Simulates a follow event.

   - **Arguments**: `<username>`.
   - **Example**:
     ```
     !debug follow NewFollower
     ```

9. **raid**: Simulates a raid.

   - **Arguments**: `<username>` `<viewercount>`.
   - **Example**:
     ```
     !debug raid RaiderUser 25
     ```

10. **shoutout-give**: Simulates giving a shoutout.

    - **Arguments**: `<username>` `<viewercount>`.
    - **Example**:
      ```
      !debug shoutout-give AmazingStreamer 50
      ```

11. **shoutout-receive**: Simulates receiving a shoutout.

    - **Arguments**: `<username>` `<viewercount>`.
    - **Example**:
      ```
      !debug shoutout-receive GenerousStreamer 30
      ```

12. **bits**: Simulates a bit donation.

    - **Arguments**: `<username>` `<amount>` `[message]` (optional).
    - **Examples**:
      ```
      !debug bits CheerMaster 500
      !debug bits CheerMaster 500 Great stream!
      ```

13. **Example**:

    ```
    !debug sub
    ```

### `!reload`

- **Access**: Streamer Only
- **Description**: Reloads Vayl to apply updated configurations.

---

## **Commands for All Users**

### `!game`

- **Access**: All Users
- **Description**: Displays the current game being streamed.

### `!uptime`

- **Access**: All Users
- **Description**: Displays the current stream uptime.

### `!quotes`

- **Access**: All Users
- **Description**: Displays the total number of quotes saved.

### `!quote <number>`

- **Access**: All Users
- **Description**: Displays the specified quote by its number.
- **Example**:
  ```
  !quote 5
  ```

### `!followage <user>`

- **Access**: All Users
- **Description**: Displays how long the specified user has been following the channel.
- **Example**:
  ```
  !followage SomeViewer
  ```

---
