import numpy as np

def cutData(patch, inputs):

    for ii in range(0, len(patch.scalars)):

        for jj in range(0, len(patch.scalars[ii].times)):

            time = patch.scalars[ii].times[jj]

            newPoints = np.array(np.zeros([0,3]))
            newField = np.array(np.zeros([0,1]))

            xLo = inputs.xLow
            xHi = inputs.xHigh
            yLo = inputs.yLow
            yHi = inputs.yHigh
            zLo = inputs.zLow
            zHi = inputs.zHigh

            for kk in range(0, len(time.points)):

                if (xLo >= time.points[kk, 0] <= xHi) and (yLo >= time.points[kk, 1] <= yHi) and (zLo >= time.points[kk, 2] <= zHi):

                    newPoints = np.append(newPoints, time.points[kk,:], axis=0)
                    newField = np.append(newField, time.field[kk,:], axis=0)

            patch.scalars[ii].times[jj].points = newPoints
            patch.scalars[ii].times[jj].field = newField

    for ii in range(0, len(patch.vectors)):

        for jj in range(0, len(patch.vectors[ii].times)):

            time = patch.vectors[ii].times[jj]

            newPoints = np.array(np.zeros([0,3]))
            newField = np.array(np.zeros([0,3]))

            xLo = inputs.xLow
            xHi = inputs.xHigh
            yLo = inputs.yLow
            yHi = inputs.yHigh
            zLo = inputs.zLow
            zHi = inputs.zHigh

            for kk in range(0, len(time.points)):

                if (xLo >= time.points[kk, 0] <= xHi) and (yLo >= time.points[kk, 1] <= yHi) and (zLo >= time.points[kk, 2] <= zHi):

                    newPoints = np.append(newPoints, time.points[kk,:], axis=0)
                    newField = np.append(newField, time.field[kk,:], axis=0)

            patch.vectors[ii].times[jj].points = newPoints
            patch.vectors[ii].times[jj].field = newField
