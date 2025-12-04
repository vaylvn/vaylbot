# **Phrase Check**

The **Phrase Check** system in Vayl allows you to detect specific words or symbols in chat and trigger predefined actions. It’s simple to set up yet powerful enough for complex reactions, making it perfect for quick chat interactions.

---

## **Example Setup**

```yaml
phrase:
  hello:
    type: contains
    cooldown:
      user: 5
      global: 0
    actions:
    - chat | Hello [user]!
    - sound | greet.wav
```

---

## **How It Works**

Each entry under `phrase:` defines a trigger and what should happen when it’s detected in chat.

| Key | Description |
|------|-------------|
| **type** | How the chat message is checked. <br>• `matches` → Only triggers if the message exactly matches the phrase.<br>• `contains` → Triggers if the message contains the phrase anywhere. |
| **cooldown** | Controls how often a phrase can trigger. Includes: <br>• `user` → Per-user cooldown (seconds before the same user can trigger it again).<br>• `global` → Global cooldown (seconds before anyone can trigger it again). |
| **actions** | A list of actions to perform when the phrase is detected. Each action follows standard Vayl syntax (e.g., `chat | message`, `sound | file.wav`, etc.). |

---

## **Additional Example**

Trigger a response when the exact symbol `^` is used in chat:

```yaml
phrase:
  ^:
    type: matches
    cooldown:
      user: 0
      global: 0
    actions:
    - chat | ^
```

- **Type:** Must exactly match `^`  
- **Cooldown:** No delay — can trigger freely  
- **Actions:** Sends `^` back into chat  

---

## **Tips**

- Keep phrases short and unique to prevent conflicts.  
- Use cooldowns wisely to reduce spam.  
- You can combine `user` and `global` cooldowns for balanced control.  
- Test your configuration in a private stream or debug mode before going live.  

---
