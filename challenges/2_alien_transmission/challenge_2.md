# 👽 Coding Challenge: The Alien Transmission

**Estimated time:** 1–2 hours  
**Tools:** Python, pandas, numpy, matplotlib (install whatever else you want)  
**Deliverable:** A `.py` script that prints the decoded message

---

## Background

On March 15, 2047, the Deep Space Radio Array picked up an anomalous repeating signal
originating from approximately 4.2 light-years away. The raw sensor data has been dumped
into `alien_transmission.csv` — 9 channels of radio frequency amplitude readings sampled
every 10 seconds over a 3.5-hour window.

The data is a mess. The array's onboard systems were mid-firmware-update when the signal
arrived, so the file is riddled with corrupted timestamps, null readings, duplicate rows,
and sensor ID inconsistencies. There are also spurious amplitude spikes scattered across
multiple channels — most are instrument noise, but one channel tells a different story.

The signal analysts at DSRA have one hypothesis: **the anomalous spikes in one of the
channels aren't noise. They're a message. And the encoding is simpler than you'd think.**

Your job: clean the data, find the signal, and decode the message.

---

## The File: `alien_transmission.csv`

| Column | Description |
|---|---|
| `timestamp` | UTC datetime of the reading (some are corrupted) |
| `channel_1` through `channel_6`, `channel_8`, `channel_9` | Amplitude readings, normally distributed around 50 ± 8. Some nulls. Some spurious spikes. |
| `ch_07_raw` | Channel 7 amplitude readings. Normally distributed around 50 ± 8. Some nulls. **This is the one.** |
| `sensor_id` | Should always be `RADIO-7`. Many entries are malformed. |

---

## Your Tasks

### Step 1 — Load & Audit the Data
Load the CSV and get a feel for what you're working with. How many rows? What's the null
situation? Are there duplicate records? Are all timestamps valid? Print a brief summary.

### Step 2 — Clean the Data
- Drop or flag rows with corrupted timestamps
- Remove duplicate rows (hint: near-duplicate timestamps count)
- Normalize the `sensor_id` column so all valid entries read `RADIO-7`
- Handle nulls in a sensible way — document your reasoning

### Step 3 — Find the Signal
The analysts believe the message is encoded in `ch_07_raw`. Normal background amplitude
for all channels is roughly **60 ± 22** (i.e., values between ~38 and ~92 are noise).

Plot the amplitude of `ch_07_raw` over time. Do you see anything unusual?

Find all rows where `ch_07_raw` is a significant outlier compared to background noise.
These are your signal rows. Sort them chronologically.

### Step 4 — Decode the Message
The encoding is simple: each signal spike's amplitude value is an **ASCII code**.

Convert the spike values to characters in chronological order. What does it say?

---

## Hints (try not to peek)

**Hint 1 — Finding outliers**
Values above ~90 in ch_07_raw are well outside normal range. Try filtering for spikes
significantly above the channel's mean + 2 standard deviations. But watch out — there
are red herrings in other channels too. Stay focused on channel 7.

**Hint 2 — ASCII decoding**
Python's built-in `chr()` function converts an integer to its ASCII character.
`chr(72)` → `'H'`. You'll want to cast your amplitude values to integers first.

**Hint 3 — Ordering matters**
The message only makes sense if the signal rows are in chronological order. Make sure
your timestamps are parsed as datetimes before sorting.

---

## What a Correct Solution Looks Like

Your script should:
1. Load `alien_transmission.csv`
2. Print a data quality summary (row count, null counts, duplicate count)
3. Clean the data (document choices inline with comments)
4. Produce a plot of `ch_07_raw` amplitude over time with signal spikes highlighted
5. Print the decoded message to stdout

A correct run ends with something like:
```
📡 Decoded transmission: "?????????????????"
```

No spoilers here. You'll know it when you see it.

---

## Bonus Challenges (if you finish early)

- **Bonus 1:** The signal spikes appear at a regular interval in the original timeline.
  Can you figure out what that interval is (in seconds)?
- **Bonus 2:** Write a function that could *encode* an arbitrary message back into a
  transmission file using the same scheme. Send the aliens a reply.
- **Bonus 3:** Channels 2, 4, and 6 also have spurious large spikes. Are they noise,
  or could they encode something too? Investigate and explain your conclusion.

---

*Good luck. They're waiting.*
