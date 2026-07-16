# Designing a Logger Framework — LLD Q&A

**Run:** `python -m lld.logger.main`  
**Patterns:** Singleton · Chain of Responsibility · Observer · Strategy

---

## Q1. What problem are we solving?

**A.** Design a configurable logging framework (Log4j/SLF4J style) that:

1. Logs at multiple **severity levels** (DEBUG → FATAL)
2. Routes each level to subscribed **appenders** (console, file)
3. Formats messages independently (**plain text** / **JSON**)
4. Exposes a simple global API: `logger.info(...)`, `logger.error(...)`

---

## Q2. What are the core entities?

| Entity | Responsibility |
|--------|----------------|
| `Logger` | Singleton facade — builds `LogMessage`, dispatches to chain |
| `LogHandler` | Chain node per level; holds subscribed appenders |
| `LogAppender` | Output sink (Console / File) |
| `LogFormatter` | Message format strategy (Plain / JSON) |
| `LogMessage` | Level + text + timestamp |
| `LogHandlerConfiguration` | Wires chain + appender subscriptions |

---

## Q3. How is the package structured?

```
logger/
├── logger.py                    # Singleton API
├── log_handler_configuration.py # Wire-up
├── model/                       # LogMessage
├── handlers/                    # Debug → Info → Warn → Error → Fatal
├── appenders/                   # ConsoleAppender, FileAppender
├── formatter/                   # PlainText, Json
└── enums/                       # LogLevel
```

---

## Q4. Why Chain of Responsibility?

**A.** Handlers are linked: `DEBUG → INFO → WARN → ERROR → FATAL`. Each tries to handle its level; otherwise passes downstream.

```python
def handle(self, message):
    if self.can_handle(message.level):
        self.notify_observers(message)
    elif self.next is not None:
        self.next.handle(message)
```

**Note:** Exact level match (not "this level and above").

---

## Q5. Why Observer on handlers?

**A.** Appenders **subscribe** to handlers. When a handler matches, it notifies all subscribed appenders.

Demo: INFO → console only; ERROR → console **and** file.

Adding a new destination = new appender + subscribe — no change to Logger.

---

## Q6. Why Strategy for formatters?

**A.** Same appender can use different formats:

```python
ConsoleAppender(PlainTextFormatter())
FileAppender(JsonFormatter())
```

---

## Q7. Why Singleton for Logger?

**A.** One global logger instance for the app — typical logging API.

```python
Logger.get_instance().error("something failed")
```

---

## Q8. What is the log flow?

```
logger.error("msg")
  → LogMessage(ERROR, msg, timestamp)
  → DebugHandler → pass → ... → ErrorHandler matches
  → notify appenders → formatter.format() → print / write
```

---

## Q9. How do you extend this design?

| Add… | How |
|------|-----|
| Syslog / Kafka appender | Implement `LogAppender` |
| Async logging | Queue + worker thread in FileAppender |
| Level threshold | Change `can_handle` to `level >= threshold` |
| Config file | Externalize `LogHandlerConfiguration` |

---

## Q10. Common interview follow-ups

**Q. Chain vs single handler with filter?**  
Chain makes per-level appender routing natural (ERROR to file, INFO to console). Threshold style is simpler for "log everything ≥ WARN".

**Q. FileAppender thread safety?**  
Uses `threading.Lock` around writes.

**Q. TRACE level?**  
Exists in enum but no `TraceHandler` wired in this demo.
