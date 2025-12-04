# **Actions (v2)**

Each action defines what Vayl should do when triggered by an event.

All actions follow the format:
```yaml
[action] | <required_arg> | [optional_arg]
```

**Syntax Key:**
- `<arg>` → Required argument  
- `[arg]` → Optional argument  
- Arguments are separated by vertical bars (`|`)  
- All actions support the [Tag System](tags.md) — e.g., `[user]`, `[counter:name]`, `[text:name]`, etc.

---

## 🧩 **OBS Integration**

<details><summary><strong>obs:scene</strong> — Switch to a specific OBS scene</summary>

**Syntax:**
```yaml
obs:scene | <scene_name>
```
**Example:**
```yaml
- obs:scene | Starting Soon
```
</details>

<details><summary><strong>obs:show</strong> — Show an OBS source</summary>

**Syntax:**
```yaml
obs:show | <source>
```
**Example:**
```yaml
- obs:show | Webcam
```
</details>

<details><summary><strong>obs:hide</strong> — Hide an OBS source</summary>

**Syntax:**
```yaml
obs:hide | <source>
```
**Example:**
```yaml
- obs:hide | AlertBox
```
</details>

<details><summary><strong>obs:toggle</strong> — Toggle visibility of an OBS source</summary>

**Syntax:**
```yaml
obs:toggle | <source>
```
**Example:**
```yaml
- obs:toggle | ChatOverlay
```
</details>

<details><summary><strong>obs:image</strong> — Change the image file for an image source</summary>

**Syntax:**
```yaml
obs:image | <source> | <file_path>
```
**Example:**
```yaml
- obs:image | Overlay | images/new_banner.png
```
</details>

<details><summary><strong>obs:label</strong> — Update a label’s text, color, or style</summary>

**Syntax:**
```yaml
obs:label | <source> | <text> | [color] | [size] | [font]
```
**Example:**
```yaml
- obs:label | StreamTitle | Live Now! | #00FF00 | 18 | Roboto
```
</details>

<details><summary><strong>obs:mediafile</strong> — Change a media source’s file</summary>

**Syntax:**
```yaml
obs:mediafile | <source> | <file_path>
```
**Example:**
```yaml
- obs:mediafile | IntroVideo | videos/start.mp4
```
</details>

<details><summary><strong>obs:slideshow</strong> — Control a slideshow source</summary>

**Syntax:**
```yaml
obs:slideshow | <source> | <state>
```
**Example:**
```yaml
- obs:slideshow | Highlights | next
```
</details>

<details><summary><strong>obs:filteron</strong> — Enable a source filter</summary>

**Syntax:**
```yaml
obs:filteron | <source> | <filter>
```
**Example:**
```yaml
- obs:filteron | Webcam | Blur
```
</details>

<details><summary><strong>obs:filteroff</strong> — Disable a source filter</summary>

**Syntax:**
```yaml
obs:filteroff | <source> | <filter>
```
**Example:**
```yaml
- obs:filteroff | Webcam | Blur
```
</details>

<details><summary><strong>obs:audio</strong> — Adjust an audio source’s volume</summary>

**Syntax:**
```yaml
obs:audio | <source> | <percentage> | <steps> | <duration>
```
**Example:**
```yaml
- obs:audio | Music | 50 | 5 | 2
```
</details>

---

## 💬 **Chat & Moderation**

<details><summary><strong>chat:message</strong> — Send a message in chat</summary>

**Syntax:**
```yaml
chat:message | <message>
```
**Example:**
```yaml
- chat:message | Welcome to the stream, [user]!
```
</details>

<details><summary><strong>chat:announce</strong> — Send a Twitch announcement</summary>

**Syntax:**
```yaml
chat:announce | <message>
```
**Example:**
```yaml
- chat:announce | Stream starting soon!
```
</details>

<details><summary><strong>vip:add</strong> — Add a Twitch VIP</summary>

**Syntax:**
```yaml
vip:add | <username>
```
**Example:**
```yaml
- vip:add | LoyalViewer
```
</details>

<details><summary><strong>vip:remove</strong> — Remove a Twitch VIP</summary>

**Syntax:**
```yaml
vip:remove | <username>
```
**Example:**
```yaml
- vip:remove | TroubleMaker
```
</details>

<details><summary><strong>timeout</strong> — Timeout a user</summary>

**Syntax:**
```yaml
timeout | <username> | <duration> | [reason]
```
**Example:**
```yaml
- timeout | [user] | 300 | Spam detected
```
</details>

<details><summary><strong>stream:clip</strong> — Create a Twitch clip</summary>

**Syntax:**
```yaml
stream:clip
```
**Example:**
```yaml
- stream:clip
```
</details>

<details><summary><strong>stream:marker</strong> — Add a stream marker</summary>

**Syntax:**
```yaml
stream:marker
```
**Example:**
```yaml
- stream:marker
```
</details>

<details><summary><strong>stream:raid</strong> — Raid another streamer</summary>

**Syntax:**
```yaml
stream:raid | <username>
```
**Example:**
```yaml
- stream:raid | FriendlyStreamer
```
</details>

<details><summary><strong>redeem:create</strong> — Create a channel point reward</summary>

**Syntax:**
```yaml
redeem:create | <name>
```
**Example:**
```yaml
- redeem:create | Hydrate
```
</details>

<details><summary><strong>redeem:enable</strong> — Enable a channel point reward</summary>

**Syntax:**
```yaml
redeem:enable | <name>
```
**Example:**
```yaml
- redeem:enable | Hydrate
```
</details>

<details><summary><strong>redeem:disable</strong> — Disable a channel point reward</summary>

**Syntax:**
```yaml
redeem:disable | <name>
```
**Example:**
```yaml
- redeem:disable | Hydrate
```
</details>

<details><summary><strong>redeem:toggle</strong> — Toggle a channel point reward</summary>

**Syntax:**
```yaml
redeem:toggle | <name>
```
**Example:**
```yaml
- redeem:toggle | Hydrate
```
</details>

---

## 🔢 **Variables**

<details><summary><strong>text:set</strong> — Set a text variable</summary>

**Syntax:**
```yaml
text:set | <name> | <text>
```
**Example:**
```yaml
- text:set | status | Stream is live!
```
</details>

<details><summary><strong>text:prepend</strong> — Prepend text to a variable</summary>

**Syntax:**
```yaml
text:prepend | <name> | <text>
```
**Example:**
```yaml
- text:prepend | title | Live - 
```
</details>

<details><summary><strong>text:append</strong> — Append text to a variable</summary>

**Syntax:**
```yaml
text:append | <name> | <text>
```
**Example:**
```yaml
- text:append | chatlog | [user]: [user_input]
```
</details>

<details><summary><strong>text:clear</strong> — Clear text from a variable</summary>

**Syntax:**
```yaml
text:clear | <name>
```
**Example:**
```yaml
- text:clear | chatlog
```
</details>

<details><summary><strong>integer</strong> — Modify an integer variable using an equation</summary>

**Syntax:**
```yaml
integer | <name> | <equation>
```
**Example:**
```yaml
- integer | score | value + 10
```
</details>

<details><summary><strong>table</strong> — Modify a table variable</summary>

**Syntax:**
```yaml
table | <name> | <entry> | <value>
```
**Example:**
```yaml
- table | stats | accuracy | 98%
```
</details>

<details><summary><strong>list:append</strong> — Add an item to a list</summary>

**Syntax:**
```yaml
list:append | <name> | <text>
```
**Example:**
```yaml
- list:append | viewers | [user]
```
</details>

<details><summary><strong>list:prepend</strong> — Add an item to the start of a list</summary>

**Syntax:**
```yaml
list:prepend | <name> | <text>
```
**Example:**
```yaml
- list:prepend | queue | [user]
```
</details>

<details><summary><strong>list:remove</strong> — Remove an item from a list</summary>

**Syntax:**
```yaml
list:remove | <name> | <text>
```
**Example:**
```yaml
- list:remove | viewers | [user]
```
</details>

<details><summary><strong>list:removeall</strong> — Remove all matching items from a list</summary>

**Syntax:**
```yaml
list:removeall | <name> | <text>
```
**Example:**
```yaml
- list:removeall | queue | [user]
```
</details>

<details><summary><strong>list:clear</strong> — Clear all items from a list</summary>

**Syntax:**
```yaml
list:clear | <name>
```
**Example:**
```yaml
- list:clear | queue
```
</details>

<details><summary><strong>boolean:true</strong> — Set a boolean to true</summary>

**Syntax:**
```yaml
boolean:true | <name>
```
**Example:**
```yaml
- boolean:true | stream_active
```
</details>

<details><summary><strong>boolean:false</strong> — Set a boolean to false</summary>

**Syntax:**
```yaml
boolean:false | <name>
```
**Example:**
```yaml
- boolean:false | stream_active
```
</details>

<details><summary><strong>boolean:toggle</strong> — Toggle a boolean value</summary>

**Syntax:**
```yaml
boolean:toggle | <name>
```
**Example:**
```yaml
- boolean:toggle | stream_active
```
</details>

---

## ⚙️ **Utility**

<details><summary><strong>playsound</strong> — Play a sound file</summary>

**Syntax:**
```yaml
playsound | <sound_name>
```
**Example:**
```yaml
- playsound | alert.wav
```
</details>

<details><summary><strong>wait</strong> — Pause execution</summary>

**Syntax:**
```yaml
wait | <seconds>
```
**Example:**
```yaml
- wait | 5
```
</details>

<details><summary><strong>syscmd</strong> — Execute a system command</summary>

**Syntax:**
```yaml
syscmd | <command>
```
**Example:**
```yaml
- syscmd | echo Hello World
```
</details>

<details><summary><strong>actionpack</strong> — Run a predefined action pack</summary>

**Syntax:**
```yaml
actionpack | <name>
```
**Example:**
```yaml
- actionpack | on_sub
```
</details>

<details><summary><strong>notify</strong> — Display a notification</summary>

**Syntax:**
```yaml
notify | <text>
```
**Example:**
```yaml
- notify | Event triggered successfully!
```
</details>

---

## 🧠 **Advanced / System**

<details><summary><strong>conditional</strong> — Trigger a conditional</summary>

**Syntax:**
```yaml
conditional | <name>
```
**Example:**
```yaml
- conditional | hype_start
```
**Learn more:** See the [Conditionals Reference](conditionals.md).
</details>

<details><summary><strong>webhook</strong> — Trigger a webhook</summary>

**Syntax:**
```yaml
webhook | <name>
```
**Example:**
```yaml
- webhook | discord_notify
```
</details>

<details><summary><strong>tts</strong> — Speak a message using Text-to-Speech</summary>

**Syntax:**
```yaml
tts | <voice> | <message> | <halt> | [limit]
```
**Example:**
```yaml
- tts | brian | [user] says, [user_input] | true | 500
```
</details>
