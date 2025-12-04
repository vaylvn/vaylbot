# Conditional Actions

Conditional actions in **Vayl** allow you to create logic-based behavior for your chatbot. These actions evaluate Python-style expressions, executing specific actions based on whether the condition evaluates to `true` or `false`.

---

## How Conditionals Work

Each conditional has three key components:
1. **Condition**: A Python expression that determines the logical outcome (`true` or `false`).
2. **True Actions**: A list of actions executed if the condition evaluates to `true`.
3. **False Actions**: A list of actions executed if the condition evaluates to `false`.

### Syntax
If working on an individual conditional `(conditionals/conditional_name.yml)`:
```yaml
condition: "<if-statement expression>"
true:
- <action_1> ; <arguments>
- <action_2> ; <arguments>
false:
- <action_3> ; <arguments>
```
If working on a nested conditional `("conditional_name" within conditionals/conditional_name.yml)`:
```yaml
conditional_name:
    condition: "<if-statement expression>"
    true:
    - <action_1> ; <arguments>
    - <action_2> ; <arguments>
    false:
    - <action_3> ; <arguments>
```

---

## Tags for Fetching Information

The following tags can be used within a condition to dynamically fetch information:

### General Tags
- `[rfollower]`: Returns a random follower's username.
- `[ruser]`: Returns a random user from the chat.
- `[system:dateus]`: Returns the current date in US format (MM/DD/YYYY).
- `[system:dateuk]`: Returns the current date in UK format (DD/MM/YYYY).
- `[system:time]`: Returns the current time in HH:MM:SS format.
- `[uptime:seconds]`: Returns the total stream uptime in seconds.

### Variables
- `[counter:name]`: Returns the value of the counter file called `name`.
- `[text:name]`: Returns the value of the text file called `name`.
- `[boolean:name]`: Returns the value of the boolean file called `name`.
- `[list:name]`: Returns the value of the list file called `name`.

### Randomization
- `[rnumber:min-max]`: Returns a random number within the given range.
- `[rlist:name]`: Returns a random item from the specified list.

### String Manipulation
- `[xstring:text:amount]`: Returns the given `text` repeated `amount` times.

---

## Example Conditionals

### Example 1: `conditionals/test.yml`
```yaml
condition: '[rnumber:10-30] > 50'
true:
- chat ; Number is higher!
false:
- chat ; Number is lower or equal to
```

- **Condition**: `[rnumber:10-30] > 50` checks if a random number between 10 and 30 is greater than 50.
- **True Actions**: Sends the chat message: `"Number is higher!"`
- **False Actions**: Sends the chat message: `"Number is lower or equal to"`

---

### Example 2: `conditionals/healthcheck.yml`
```yaml
condition: '[counter:health] < 20 and [text:status] == "paralysed"'
true:
- chat ; Player is on low health AND paralysed!
false: []
```

- **Condition**: `[counter:health] < 20 and [text:status] == "paralysed"`
  - Checks if the `health` counter is below 20 and the `status` variable equals `"paralysed"`.
- **True Actions**: Sends the chat message: `"Player is on low health AND paralysed!"`
- **False Actions**: No actions are taken.

---

## Supported Operators in Conditions

You can use the following operators in your conditions:
- **Comparison**: `<`, `>`, `<=`, `>=`, `==`, `!=`
- **Logical**: `and`, `or`, `not`
- **Arithmetic**: `+`, `-`, `*`, `/`

---

## Using Conditional Actions in Vayl

To trigger a conditional, you can now use either of the following formats:

### 1. Individual Conditional File
```yaml
conditional ; conditional_name
```
This format refers to a standalone file (e.g., `conditionals/conditional_name.yml`) for evaluating the conditional.

### 2. Conditional Within a File
```yaml
conditional ; file_name:conditional_name
```
This format allows you to reference a specific conditional within a file (e.g., `conditionals/file_name.yml`).

### Example
```yaml
actions:
- conditional ; test
```
This triggers the `test` conditional from the `conditionals/test.yml` file.
```yaml
actions:
- conditional ; healthcheck:low_health
```
This triggers the `low_health` conditional from the `conditionals/healthcheck.yml` file.

---

## Best Practices

- **Test Conditions**: Ensure your conditions use valid Python syntax and reference existing tags, counters, or text variables.
- **Organize Tags**: Use descriptive names for variables and counters for better clarity.
- **Simplify Logic**: Avoid overly complex conditions to make debugging easier.

---

With conditional actions and tags, Vayl allows for dynamic and interactive functionality in your Twitch chat, tailored to your specific needs. Combine these features with other actions for a fully automated and intelligent chatbot.

