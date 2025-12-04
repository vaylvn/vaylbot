# **Vayl Bot Quickstart Guide**

This guide will get your bot running in just a few minutes.

---

## **Step 1: Download Vayl**

1. Visit the [Vayl Bot GitHub Releases](https://github.com/vaylvn/vaylbot/releases/latest).
2. Download the **latest ZIP file**
3. Extract it to a folder on your PC (e.g., `C:\Vayl`).

---

## **Step 2: Configure the Bot**

1. Open the folder you just extracted.
2. Navigate to:  
   ```
   configuration\configuration.yml
   ```
3. Open it in your preferred text editor (Notepad, Notepad++, VS Code, etc.).
4. Update the following fields as needed:

### **Basic Setup**
```yaml
connected-account: your-twitch-username
bug-auto-report: true
```
- `connected-account`: Your Twitch username (lowercase).
- `bug-auto-report`: Set to `false` if you prefer not to send crash reports.

### **OBS Integration (optional)**
```yaml
obs:
  host: localhost
  port: 4455
  password: your-obs-password
```
If you use **OBS WebSocket**, configure this section accordingly.  
(Older `obs-password` format is deprecated — update to this format.)

---

## **Step 3: Run Vayl**

1. Double-click `Vayl.exe`.
2. When prompted, a browser window will open for Twitch authorization.  
   Grant permissions so the bot can:
   - Listen for Twitch events (subs, follows, raids, etc.)
   - Send chat messages and announcements
3. Once authorized, you can close the browser tab — setup will complete automatically.

---

## **Step 4: Verify and Customize**

After the first launch, Vayl will generate its default folders:

```
configuration/
data/
variables/
```

You can now begin customizing:
- **Events:** Set up responses to Twitch events in `data/events/`
- **Actions:** Define command or timed actions using `.yml` files
- **Variables:** Create counters, booleans, and text files in `data/variables/`

---

## **Step 5: Reload or Restart**

- Most changes (actions, event triggers) reload automatically.  
- Some configurations (commands, moderation, PhraseCheck) require a restart.  
- You can also type `!reload` in chat to reload configurations manually.

---

## **Next Steps**

Explore these guides to unlock Vayl’s full potential:
- [Actions Guide](actions.md)
- [Conditional Actions](conditional-actions.md)
- [Events Guide](events.md)
- [TTS Setup](tts.md)
- [PhraseCheck](phrasecheck.md)

---

