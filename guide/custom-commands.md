# **Custom Commands**
Looking for [Default Commands?](default-commands.md)

Vayl Bot allows users to create and manage custom commands to extend functionality and tailor the bot's behavior to their needs. Custom commands can trigger specific actions, enforce access restrictions, and manage cooldowns.

---

## **Structure of a Custom Command**

Custom commands are defined in the `commands.yml` file located in the bot's configuration directory. Below is the structure of a custom command:

```yaml
command:
  <command_name>:
    cooldown:
      user: <time_in_seconds>
      global: <time_in_seconds>
    streamer-only: <true/false>
    sub-only: <true/false>
    mod-only: <true/false>
    vip-only: <true/false>
    actions:
    - <action>
```

### **Fields Explained**

1. **`<command_name>`**:
   - The name of the command that users will type in chat.
   - Example: `testing` for `!testing`.

2. **`cooldown`**:
   - Defines the cooldown times for the command.
     - **`user`**: Time (in seconds) before the same user can use the command again.
     - **`global`**: Time (in seconds) before anyone can use the command again.

3. **Access Restrictions**:
   - **`streamer-only`**: If `true`, only the streamer can use this command.
   - **`sub-only`**: If `true`, only subscribers can use this command.
   - **`mod-only`**: If `true`, only moderators can use this command.
   - **`vip-only`**: If `true`, only VIPs can use this command.

4. **`actions`**:
   - A list of actions the command will trigger. Actions can include variable tags and integrations like OBS.

---

## **Example Custom Command**

### **Command Definition**

```yaml
command:
  testing:
    cooldown:
      user: 0
      global: 5
    streamer-only: false
    sub-only: false
    mod-only: false
    vip-only: false
    actions:
    - obs:toggle ; test
```

### **Explanation**
- **Command Name**: `testing` (triggered by typing `!testing` in chat).
- **Cooldowns**:
  - **User Cooldown**: `0` seconds (no restriction on individual users).
  - **Global Cooldown**: `5` seconds (prevents anyone from using the command for 5 seconds after it’s triggered).
- **Access Restrictions**:
  - Open to all users (`streamer-only`, `sub-only`, `mod-only`, and `vip-only` are all `false`).
- **Actions**:
  - Toggles the OBS scene item named `test`.

---

## **Using Tags in Custom Commands**

Vayl supports the use of dynamic tags within custom commands to provide personalized responses and interactions. Below are the available tags:

1. **`[user]`**:
   - Returns the username of the person who triggered the command.
   - Example: "Thank you, [user]!"

2. **`[cmdtext]`**:
   - Returns the text entered after the command.
   - Example: If a user types `!vd Hello World`, `[cmdtext]` will return "Hello World."

3. **`[arg1]`, `[arg2]`, `[arg3]`, etc.**:
   - Refers to individual arguments in the command text.
   - Example: If a user types `!vd Hello World`, `[arg1]` will return "Hello," and `[arg2]` will return "World."

---

## **Creating Advanced Commands**

1. **Using Multiple Actions**:
   - Custom commands can trigger multiple actions sequentially:
     ```yaml
     command:
       multi:
         cooldown:
           user: 10
           global: 20
         streamer-only: false
         sub-only: false
         mod-only: false
         vip-only: false
         actions:
         - chat ; Welcome, [user]!
         - obs:scene ; Gaming Scene
         - playsound ; notification
     ```

2. **Adding Variables**:
   - Use dynamic placeholders to personalize responses:
     ```yaml
     command:
       greet:
         streamer-only: false
         sub-only: false
         mod-only: false
         vip-only: false
         cooldown:
           user: 5
           global: 5
         actions:
         - chat ; Hello, [user]! Welcome to the stream.
     ```

---

## **Testing Custom Commands**

1. Add your custom command to the `commands.yml` file.
2. Restart Vayl or use the `!reload` command in chat to apply the changes.
3. Test the command in your Twitch chat to ensure it behaves as expected.

---

## **Best Practices**

1. **Set Appropriate Cooldowns**:
   - Prevent spam by setting reasonable cooldowns for frequently used commands.

2. **Restrict Access When Needed**:
   - Use access toggles (`streamer-only`, `mod-only`, etc.) for commands that should not be available to all users.

3. **Test Commands Thoroughly**:
   - Test each command in a controlled environment to avoid issues during live streams.

