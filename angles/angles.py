import csv
import sys
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    print("Usage: python3 angles.py <csv_file>")
    sys.exit(1)

csv_file = sys.argv[1]
angles = []
distances = []

with open(csv_file, newline="") as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Skip the header row
    for row in reader:
        if not row or len(row) < 2:
            continue
        try:
            angle = float(row[0])
            distance = float(row[1])
            angles.append(angle)
            distances.append(distance)
        except ValueError:
            continue  # skip malformed lines

plt.figure(figsize=(10, 5))
plt.plot(angles, distances, marker="o", linestyle="-")
plt.xlabel("Angle (radians)")
plt.ylabel("Distance")
plt.title("Distances at Each Angle")
plt.grid(True)
plt.show()
