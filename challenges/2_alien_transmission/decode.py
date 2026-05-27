import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

csv_path = 'alien_transmission.csv'

# Load all data into data frame
df = pd.read_csv(csv_path)
# Count rows
print(f" Original rows: {len(df)}")
print("\nNull counts:")
print(df.isnull().sum())
print(f"\nExact duplicate rows: {df.duplicated().sum()}")

# Turns timestamp column into datetime values.
# Chech for curropted timestamps and turn it into Not a time value.
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Count bad timestamps
bad_timestamps = df["timestamp"].isnull().sum()

print(f"\nBad timestamps: {bad_timestamps}")

# Remove rows with bad timestamps
df = df.dropna(subset=["timestamp"])

# Remove rows where channel 7 is missing
df = df.dropna(subset=["ch_07_raw"])

print(f"\nRows after cleaning: {len(df)}")



#rows where channel 7 has large values
signal_rows = df[df["ch_07_raw"] > 92]

# Put signal rows in order
signal_rows = signal_rows.sort_values("timestamp")

print("\nSignal Rows:")
print(signal_rows[["timestamp", "ch_07_raw"]])



# Plot all channel 7 values over time
plt.figure(figsize=(12,6))

plt.plot(df["timestamp"],
          df["ch_07_raw"],
          color = "yellow",
          label="Channel 7")

# Highlight signal spikes in red
plt.scatter(
    signal_rows["timestamp"],
    signal_rows["ch_07_raw"],
    color="black",
    label="Signal Spikes"
)

# labels
plt.title("Alien Transmission Signal")
plt.xlabel("Timestamp")
plt.ylabel("Amplitude")

plt.legend()

# show graph
plt.show()



# Turn spike amplitudes into integers
ascii_values = signal_rows["ch_07_raw"].astype(int)

# Convert ASCII numbers into letters
message = ""

for value in ascii_values:
    message += chr(value)

# Print final decoded message
print("\nDecoded Message:")
print(message)

