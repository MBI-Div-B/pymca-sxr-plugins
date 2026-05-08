try:
    from PyMca5.PyMcaCore import Plugin1DBase
except ImportError:
    from . import Plugin1DBase

from PyMca5.PyMcaGui import PyMcaQt as qt

import numpy as np

class SkipPointsPlugin(Plugin1DBase.Plugin1DBase):
    def __init__(self, plotWindow, **kw):
        Plugin1DBase.Plugin1DBase.__init__(self, plotWindow, **kw)
        # method names
        self.ploltWindow = plotWindow
        self._method_even = "Display even data points"
        self._method_odd = "Display odd data points"
        self._method_odd_and_even = "Display odd and even data points"
        self._method_odd_and_even_avg = "Display odd and even average"

    def getMethods(self, plottype=None):
        # display method names
        return [self._method_even, self._method_odd, self._method_odd_and_even, self._method_odd_and_even_avg]

    def applyMethod(self, methodName):
        # get data point of active curve
        activeCurve = self.getActiveCurve()
        if activeCurve is None:
            allCurves = self.getAllCurves()
            if not allCurves:
                msg = qt.QMessageBox(self.plotWindow)
                msg.setWindowTitle("No Data")
                msg.setText("There are no curves to edit.")
                msg.exec()
                return
            activeCurve = allCurves[0]

        x, y, legend, info = activeCurve[:4]

        if methodName == self._method_even:
            x_new = x[::2]
            y_new = y[::2]
            new_legend = legend + "_even"
            self.addCurve(x_new, y_new, legend=new_legend, replace=False)
        elif methodName == self._method_odd:
            x_new = x[1::2]
            y_new = y[1::2]
            new_legend = legend + "_odd"
            self.addCurve(x_new, y_new, legend=new_legend, replace=False)
        elif methodName == self._method_odd_and_even:
            x_new_odd = x[1::2]
            y_new_odd = y[1::2]
            x_new_even = x[::2]
            y_new_even = y[::2] 
            new_legend_odd = legend + "_odd"
            new_legend_even = legend + "_even"
            self.addCurve(x_new_odd, y_new_odd, legend=new_legend_odd, replace=False)
            self.addCurve(x_new_even, y_new_even, legend=new_legend_even, replace=False)
        elif methodName == self._method_odd_and_even_avg:
            x_new_odd = x[1::2]
            y_new_odd = np.mean(y[1::2])
            x_new_even = x[::2]
            y_new_even = np.mean(y[::2])
            new_legend_odd = legend + "_odd"
            new_legend_even = legend + "_even"
            self.addCurve(x_new_odd, y_new_odd, legend=new_legend_odd, replace=False)
            self.addCurve(x_new_even, y_new_even, legend=new_legend_even, replace=False)
        else:
            return
        

MENU_TEXT = "Skip Points Plugin"

def getPlugin1DInstance(plotWindow, **kw):
    return SkipPointsPlugin(plotWindow, **kw)