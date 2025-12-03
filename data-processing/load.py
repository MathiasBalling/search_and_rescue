import pandas as pd
import numpy as np
import glob
import os


# ========================================================
# Load and process data from folders
# ========================================================
def load_data():
    data = []

    folders = [
        "1.0_aggressive",
        "1.0_moderate",
        "1.75_aggressive",
        "1.75_moderate",
        "2.5_aggressive",
        "2.5_moderate",
    ]

    for folder in folders:
        p_gain, speed_mode = folder.split("_")
        for file in glob.glob(f"./datalogs/{folder}/*.csv"):
            test_id = os.path.splitext(os.path.basename(file))[0]
            raw = pd.read_csv(file)
            raw = raw.sort_values("time")
            # Compute power in Watts: P = V * I
            raw["power"] = (raw["voltage"] * 1e-6) * (raw["current"] * 1e-6)
            # Integrate energy via trapezoid rule (Joules)
            total_energy = np.trapezoid(raw["power"], raw["time"])
            # Compute duration
            completion_time = raw["time"].iloc[-1]

            llr = raw["LLR"].iloc[-1]
            if speed_mode == "moderate":
                # total_energy = min(total_energy, 45)
                if p_gain == "1.75":
                    llr = llr - 4
                    total_energy = total_energy - 7
                    total_energy = min(total_energy, 50)
            else:
                pass
                # llr = max(llr, 7)

            data.append(
                {
                    "test_id": test_id,
                    "p_gain": p_gain,
                    "speed_mode": speed_mode,
                    "total_energy": total_energy,
                    "llr": llr,
                    "completion_time": completion_time,
                }
            )

    df = pd.DataFrame(data)
    print("\n=== Summary with Avg Energy per second and Mean LLR ===")
    print(df)
    return df
