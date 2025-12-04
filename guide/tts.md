# **Text-to-Speech (TTS)**

The **TTS** system in Vayl allows your bot to speak messages aloud using a variety of online voice engines.  
It supports multiple voice packs and provides fine control over message behavior, timing, and limits.

---

## **Syntax**

```yaml
tts | [voice_name] | [message] | [halt] | [char_limit]
```

### **Example**

```yaml
- tts | Ivy | [user_input] | true | 500
```

| Parameter | Description |
|------------|-------------|
| **voice_name** | The name or ID of the TTS voice to use. |
| **message** | The text to speak. You can use Vayl tags (e.g., `[user]`, `[counter:name]`, etc.). |
| **halt** | Whether to wait (`true`) or continue (`false`) while the TTS plays. |
| **char_limit** | Maximum character length before skipping playback. |

---

## **Pronunciation Overrides**

Custom word pronunciations can be defined in your `pronunciation.yml` file:

```yaml
valonvn: valon vee en
swdofberserk: sword of berserk
```

Vayl will automatically substitute these pronunciations in any TTS message.

---

## **Supported Voice Packs**

Vayl currently supports three TTS systems.  
Click each to view their available voices.

---

<details>
<summary><strong>Oddcast</strong></summary>

*(These voices use numeric IDs, e.g. “4-3-1”)*  
<sub>Note: Not all Oddcast voices may function due to API deprecation.</sub>

```
4-3-1, 6-2-1, 5-4-1, 4-2-1, 5-3-1, 2-7-1, 1-7-1, 7-4-1, 5-2-1, 12-4-1, 8-4-1, 9-2-1, 10-2-1, ...
```
(Full list maintained in source code for reference.)
</details>

---

<details>
<summary><strong>StreamElements</strong></summary>

```
Brian, Amy, Emma, Geraint, Russell, Nicole, Joey, Justin, Matthew, Ivy, Joanna, Kendra, Kimberly, Salli, Raveena, Zhiyu, Mads, Naja, Ruben, Lotte, Mathieu, Celine, Chantal, Hans, Marlene, Vicki, Aditi, Karl, Dora, Carla, Bianca, Giorgio, Takumi, Mizuki, Seoyeon, Liv, Ewa, Maja, Jacek, Jan, Ricardo, Vitoria, Cristiano, Ines, Carmen, Maxim, Tatyana, Enrique, Conchita, Mia, Miguel, Penelope, Astrid, Filiz, Gwyneth, en-US-Wavenet-A, en-US-Wavenet-B, en-GB-Wavenet-A, en-GB-Wavenet-D, it-IT-Wavenet-A, ja-JP-Wavenet-A, ko-KR-Wavenet-A, ru-RU-Wavenet-B, es-ES-Standard-A, tr-TR-Wavenet-B, vi-VN-Wavenet-A, ...
```
</details>

---

<details>
<summary><strong>Streamlabs</strong></summary>

```
Brian, Amy, Emma, Geraint, Russell, Nicole, Joey, Justin, Matthew, Ivy, Joanna, Kendra, Kimberly, Salli, Raveena, Zhiyu, Mads, Naja, Ruben, Lotte, Mathieu, Celine, Chantal, Hans, Marlene, Vicki, Aditi, Karl, Dora, Carla, Bianca, Giorgio, Takumi, Mizuki, Seoyeon, Liv, Ewa, Maja, Jacek, Jan, Ricardo, Vitoria, Cristiano, Ines, Carmen, Maxim, Tatyana, Enrique, Conchita, Mia, Miguel, Penelope, Astrid, Filiz, Gwyneth
```
</details>

---

## **Usage Examples**

### Basic Message
```yaml
- tts | Brian | Hello [user], welcome to the stream! | true | 250
```

### Custom Pronunciations
```yaml
- tts | Amy | Thanks [user] for the sub! | false | 200
```

### Character Limit Example
```yaml
- tts | Ivy | This message is too long and will be skipped if over 500 characters. | true | 500
```

---

## **Notes & Recommendations**

- Use **StreamElements** or **Streamlabs** for reliable modern TTS support.  
- **Oddcast** remains for legacy compatibility but may break depending on API uptime.  
- Keep messages under 300 characters for best performance.  
- Test new voices before using them live.  
- Combine TTS with chat or sound actions for layered reactions.

---
