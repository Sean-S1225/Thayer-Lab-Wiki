import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as patches
import pandas as pd
import numpy as np
from matplotlib.colors import ListedColormap

def PlotSecStructMatrices(RepName, titleNames, systems, directory, fileName = "SecStructMatrix.png", comparison = True):
    secStructColorDict = {0: "#ffffff",
                        1: "#0000ff",
                        2: "#00ff00",
                        3: "#00ffff",
                        4: "#ff0000",
                        5: "#000000",
                        6: "#ffff00",
                        7: "#ff00ff"}

    secStructNameDict = {0: "None",
                        1: "Parallel\nBeta-Sheet",
                        2: "Anti-Parallel\nBeta-Sheet",
                        3: "3-10 Helix",
                        4: "Alpha Helix",
                        5: "Pi Helix",
                        6: "Turn",
                        7: "Bend"}

    compColorDict = {"Y": "#00ff00",
                    "Boring": "#ffffff",
                    "Ny": "#ff0000",
                    "Np": "#0000ff"}

    compColorDictRGB = {"Y": [0, 255, 0],
                    "Boring": [255, 255, 255],
                    "Ny": [255, 0, 0],
                    "Np": [0, 0, 255]}

    compColorName = {"Y": "Rescued",
                    "Boring": "Identical",
                    "Ny": "Y220C ≠ WT\nY220C = PK11000",
                    "Np": "PK11000 ≠ WT\nPK11000 ≠ Y220C"}

    secStrucCMap = ListedColormap(list(secStructColorDict.values()))
    compCMap = ListedColormap(list(compColorDict.values()))

    plt.rcParams["font.family"] = "Helvetica"

    fig = plt.figure(layout='constrained', figsize=(20, 10))
    fig.suptitle("Secondary Structure", fontsize=20)
    subfigs = fig.subfigures(int((len(RepName)+1)/2), 2)

    if type(subfigs) == np.ndarray:
        subfigs = subfigs.flatten()
    else:
        subfigs = np.ndarray(shape=(1,), dtype=mpl.axes.Axes, buffer=np.array([subfigs]))

    # fig.delaxes(subfigs[-1])

    for subfig, file, title in zip(subfigs, RepName, titleNames):
        axs = subfig.subplots(1, len(systems)+comparison)
        subfig.suptitle(title, fontsize=15)

        systemData = []
        for sim in systems:
            systemData.append(pd.read_csv(directory(file, sim), sep="\s+").drop("#Frame", axis=1)[:1000])

        # wt = pd.read_csv(f"../Data/FL/FL/SecStruct/{file}_WT_SecStructTime.dat", sep="\s+").drop("#Frame", axis=1)[:1000]
        # y220c = pd.read_csv(f"../Data/FL/FL/SecStruct/{file}_Y220C_SecStructTime.dat", sep="\s+").drop("#Frame", axis=1)[:1000]
        # pk11000 = pd.read_csv(f"../Data/FL/FL/SecStruct/{file}_PK11000_SecStructTime.dat", sep="\s+").drop("#Frame", axis=1)[:1000]

        if type(axs) == np.ndarray:
            axs = axs.flatten()
        else:
            axs = np.ndarray(shape=(1,), dtype=mpl.axes.Axes, buffer=np.array([axs]))

        # arr = []
        # wtSimilarToY220C = []
        # wtSimilarToPK11000 = []
        # # y220cSimilarToPK11000 = []
        # for (_, wtSeries), (_, y220cSeries), (_, pk11000Series) in zip(wt.items(), y220c.items(), pk11000.items()):
        #     row = []
        #     tempWTSimilarToY220C = 0
        #     tempWTSimilarToPK11000 = 0
        #     for (_, wtValue), (_, y220cValue), (_, pk11000Value) in zip(wtSeries.items(), y220cSeries.items(), pk11000Series.items()):
        #         if wtValue == y220cValue:
        #             tempWTSimilarToY220C += 1
        #             if wtValue == pk11000Value:
        #                 #Boring
        #                 tempWTSimilarToPK11000 += 1
        #                 row.append(compColorDictRGB["Boring"])
        #             else:
        #                 #Np
        #                 row.append(compColorDictRGB["Np"])
        #         else:
        #             if wtValue == pk11000Value:
        #                 #Rescued
        #                 tempWTSimilarToPK11000 += 1
        #                 row.append(compColorDictRGB["Y"])
        #             else:
        #                 #Ny
        #                 row.append(compColorDictRGB["Ny"])
        #     arr.append(row)
        #     wtSimilarToY220C.append(tempWTSimilarToY220C/393)
        #     wtSimilarToPK11000.append(tempWTSimilarToPK11000/393)

        # systemData.append(arr)

        # pd.DataFrame(wtSimilarToY220C).to_csv(f"../Data/SecStruct/{file}_WT_Similar_Y220C.csv", header=False)
        # pd.DataFrame(wtSimilarToPK11000).to_csv(f"../Data/SecStruct/{file}_WT_Similar_PK11000.csv", header=False)

        # axs[0].set_title("WT")
        # axs[1].set_title("Y220C")
        # axs[2].set_title("PK11000")
        # axs[3].set_title("Comparison")

        for ax, system, systemName in zip(axs, systemData, systems):
            ax.set_title(systemName)
            im = ax.imshow(system.T.to_numpy(), cmap=secStrucCMap, aspect="auto")

            rect = patches.Rectangle((50, 50), 50, 50, color="black", fill=False)
            ax.add_patch(rect)

        # im = axs[0].imshow(wt.T.to_numpy(), cmap=secStrucCMap, aspect="auto")
        # im = axs[1].imshow(y220c.T.to_numpy(), cmap=secStrucCMap, aspect="auto")
        # im = axs[2].imshow(pk11000.T.to_numpy(), cmap=secStrucCMap, aspect="auto")
        # im2 = axs[3].imshow(arr, cmap=compCMap, aspect="auto")

        last = None
        if comparison:
            last = -1
        else:
            last = len(axs)
        cbar = plt.colorbar(im, ax = axs[:last], location="bottom")
        # cbar2 = plt.colorbar(im2, ax = axs[-1], location="right")

        numTicks = len(secStructNameDict.values())
        tick_locs = (np.arange(numTicks) + 0.5)*(numTicks-1)/numTicks
        cbar.ax.get_xaxis().set_ticks(tick_locs)
        cbar.ax.get_xaxis().set_ticklabels(list(secStructNameDict.values()))

        numTicks = len(compColorName.values())
        tick_locs = np.linspace(0, 255, numTicks+1)
        shift = (tick_locs[1] - tick_locs[0])/2
        tick_locs += shift
        tick_locs = np.delete(tick_locs, -1)
        # cbar2.ax.get_yaxis().set_ticks(tick_locs)
        # cbar2.ax.get_yaxis().set_ticklabels(list(compColorName.values()))

    fig.savefig(fileName, bbox_inches = "tight", dpi = 500)
    # plt.show()

# PlotSecStructMatrices(["12A_001_v1", "12A_001_v2", "15A_001_v1", "15A_001_v2", "15A_0005", "15A_002", "15A_00225"],
#                       ["12Å_0.001Δt_v1", "12Å_0.001Δt_v2", "15Å_0.001Δt_v1", "15Å_0.001Δt_v2", "15Å_0.0005Δt", "15Å_0.002Δt", "15Å_0.00225Δt"],
#                       ["WT", "Y220C", "PK11000"],
#                       lambda file, sim: f"../Data/FL/FL/SecStruct/{file}_{sim}_SecStructTime.dat",
#                       comparison=False)

# PlotSecStructMatrices(["Rep1", "Rep2", "Rep3", "Rep4", "Rep5", "Mark", "aff03ws", "aff03wsFL"], ["Rep1", "Rep2", "Rep3", "Rep4", "Rep5", "Mark", "aff03ws DBD", "aff03ws Full Length"],
#                       ["WT"], lambda file, sim: f"../Data/DBD/ff19SB/SecStruct/p53_DBD_ff19SB_{file}_{sim}_SecStructTime.dat",
#                       comparison=False, fileName="DBD_WT_SecStruct2.png")

PlotSecStructMatrices(["Rep1", "Rep2"], ["Rep1", "Rep2"], ["WT", "Y220C", "PK11000"], lambda file, sim: f"../Data/DBD/ff14SB/SecStruct/p53_DBD_ff14SB_{file}_{sim}_SecStructTime.dat",
                      "DBD_Mark_WT_SecStruct.png", False)