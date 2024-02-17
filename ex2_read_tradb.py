"""
Read and plot transient data
============================
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import vallenae as vae

HERE = Path(__file__).parent if "__file__" in locals() else Path.cwd()
TRADB = HERE / "1p12_Ft_25000.tradb"  # uncompressed
TRAI = 1.123456e6  # just an example, no magic here


def main():
    # Read waveform from tradb
    with vae.io.TraDatabase(TRADB) as tradb:
        y, t = tradb.read_wave(TRAI)
        print(tradb.rows())
        print(tradb.columns())
        print(tradb.tables())
        print(tradb.fieldinfo())
        print(tradb.globalinfo())
        df = tradb.iread(trai=TRAI)
        for i in df:
            print(i)
            print(i[4])
            treshold_pos = len(y)*[i[4]*1e3]
            treshold_neg = len(y)*[-i[4]*1e3]
        

    y *= 1e3  # in mV
    t *= 1e6  # for µs

    # Plot waveforms
    plt.figure(figsize=(8, 4), tight_layout=True)
    plt.plot(t, y)
    plt.plot(t, treshold_pos ,'r')
    plt.plot(t, treshold_neg, 'r')
    plt.xlabel("Time [µs]")
    plt.ylabel("Amplitude [mV]")
    plt.title(f"Transient Wave Plot; trai = {TRAI}")
    plt.show()


if __name__ == "__main__":
    main()
