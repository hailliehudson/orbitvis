from skyfield.api import load, wgs84
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    ts = load.timescale()

    # ISS from Celestrak (stations list)
    sats = load.tle_file("https://celestrak.org/NORAD/elements/stations.txt")
    sat = sats[0]
    print("Satellite:", sat.name)

    # Ground station: London
    gs = wgs84.latlon(51.5074, -0.1278)

    # Next 24 hours, 1-minute steps
    t0 = ts.now().utc_datetime()
    minutes = np.arange(0, 24 * 60, 1)
    times = ts.utc(t0 + pd.to_timedelta(minutes, unit="m"))

    # Elevation computation
    difference = sat - gs
    alt, az, distance = difference.at(times).altaz()
    elevation = alt.degrees

    # Detect passes above 10 degrees
    min_el = 10.0
    above = elevation >= min_el
    passes = []
    in_pass = False
    aos = None

    for i, is_above in enumerate(above):
        if is_above and not in_pass:
            aos = i
            in_pass = True
        elif (not is_above) and in_pass:
            los = i
            in_pass = False
            passes.append((aos, los))

    # Print pass summary
    rows = []
    for idx, (aos, los) in enumerate(passes, 1):
        seg = elevation[aos:los]
        max_el = float(np.max(seg)) if len(seg) else float("nan")
        max_i = int(aos + np.argmax(seg)) if len(seg) else aos
        rows.append({
            "pass": idx,
            "aos_utc": times[aos].utc_iso(),
            "los_utc": times[los].utc_iso(),
            "duration_min": round((los - aos), 1),
            "max_el_deg": round(max_el, 2),
            "t_max_utc": times[max_i].utc_iso(),
        })

    df = pd.DataFrame(rows)
    if df.empty:
        print("No passes above 10° found in next 24 hours.")
    else:
        print(df.to_string(index=False))
        df.to_csv("passes.csv", index=False)
        print("\nSaved passes.csv")

    # Plot elevation
    plt.figure()
    plt.plot(minutes / 60, elevation)
    plt.axhline(min_el, linestyle="--")
    plt.xlabel("Hours from now (UTC)")
    plt.ylabel("Elevation (deg)")
    plt.title(f"{sat.name} elevation from London")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()