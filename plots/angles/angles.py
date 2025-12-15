import csv
import sys
import matplotlib.pyplot as plt


def viz_angles(csv_file, title="Distances at Each Angle", show=False, save=True):
    angles = []
    distances = []

    with open(csv_file) as csvfile:
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

    plt.figure(figsize=(8, 6))
    plt.plot(angles, distances, marker="o", linestyle="-")
    plt.xlabel("Angle (radians)")
    plt.ylabel("Distance")
    plt.title(title)
    plt.grid(True)
    if save:
        plt.savefig(f"{csv_file.rsplit('.', 1)[0]}.png")
    if show:
        plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 angles.py <csv_file>")
        sys.exit(1)
    csv_file = sys.argv[1]
    viz_angles(csv_file, show=True, save=False)
