from pathlib import Path
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.ticker as mticker

from matplotlib import pyplot as plt

if __name__ == "__main__":
    df = pd.read_csv("data/1e7.dat", delim_whitespace=True, comment='#')
    age_list = list(Counter(df.age).keys())
    age_list.sort()
    age = age_list[3]
    item_p = df[df.age == age]
    item_p_sort = item_p.sort_values("Mass")
    item_p_sort = item_p_sort[(item_p_sort.logL < 3) & (item_p_sort.Mass >= 1)]


    for data_file in ["1e7.dat", "1e8.dat", "1e9.dat", "15e9.dat"]:
        df = pd.read_csv(f"data/{data_file}", delim_whitespace=True, comment='#')
        
        age_list = list(Counter(df.age).keys())
        age_list.sort()
        for i in range(len(age_list)):
            age = age_list[i]
            unit = "Gyr" if age >= 1e9 else "Myr"
            age_unit = age / 1e9 if age >= 1e9 else age / 1e6
            item = df[df.age == age]
            ratio = 1 + np.random.normal(0, 0.02, len(item))
            item = item.assign(ratio=ratio)

            fig, ax = plt.subplots(1, 1)
            ax.scatter(10 ** item.logTe * ratio, np.log10(10 ** item.logL * item.ratio), s=(4 / item.logg) ** 2, facecolors='none', edgecolors='grey', alpha=0.5) 
            item_sel = item[(item.logg >= 3.5) & (item.Mini > 1.6)]
            ratio_2 = np.random.random(len(item_sel))
            im = ax.scatter(10 ** item_sel.logTe * item_sel.ratio * (0.9 + 0.1 * ratio_2 ** 2), np.log10(10 ** item_sel.logL * item_sel.ratio) * (0.8 +  0.2 * ratio_2 ** 2), s=(4 / item_sel.logg) ** 2, c=item_sel.Mass, vmin=1, vmax=7.2) 
            item_sel = item[(item.logg < 3.5) | (item.Mini < 1.6)] 
            ax.scatter(10 ** item_sel.logTe * item_sel.ratio, np.log10(10 ** item_sel.logL * item_sel.ratio), s=(4 / item_sel.logg) ** 2, c=item_sel.Mass, vmin=1, vmax=7.2) 
            ax.plot(10 ** item_p_sort.logTe, item_p_sort.logL, c='red')
            for mass in [3.0, 2.5, 2.0, 1.5, 1.0]:
                item_p_mass = item_p_sort.loc[np.abs(item_p_sort.Mass - mass).idxmin()]
                ax.scatter(10 ** item_p_mass.logTe, item_p_mass.logL, c='red', s=8)
                ax.text(10 ** (item_p_mass.logTe + 0.05), item_p_mass.logL - 0.3, "{:.1f}".format(mass))
            ax.set_xlabel('Temperature (K)')
            ax.set_ylabel(r'Luminosity ($L_\odot$)')
            ax.set_xlim(20000, 3000)
            ax.set_ylim(-2, 5)
            ax.set_xscale("log")
            ax.set_title("Age: {0:.1f} {1}".format(age_unit, unit))
            ax.xaxis.set_minor_formatter(mticker.ScalarFormatter())
            ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
            plt.setp(ax.xaxis.get_minorticklabels(), rotation=45)
            plt.xticks(rotation=45, ha='right')
            # plt.show()
            output_folder = "figure_4"
            p = Path(output_folder)
            if not p.is_dir():
                p.mkdir(parents=True)
            plt.savefig('{0}/cmd-{1:0>3d}.png'.format(output_folder, int(age/1e7)), bbox_inches='tight')
            plt.close()

