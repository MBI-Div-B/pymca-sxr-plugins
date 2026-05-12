import numpy as np
from PyMca5.PyMcaGui import PyMcaQt as qt

try:
    from PyMca5.PyMcaCore import Plugin1DBase
except ImportError:
    from . import Plugin1DBase

class DataStatsPlugin(Plugin1DBase.Plugin1DBase):
    def __init__(self, plotWindow, **kw):
        # 1. Basisklasse initialisieren
        Plugin1DBase.Plugin1DBase.__init__(self, plotWindow, **kw)
        
        # 2. EXPLIZITE ZUWEISUNG (behebt den AttributeError)
        self.plotWindow = plotWindow
        
        self._methodName = "Average and STD of Curves"

    def getMethods(self, plottype=None):
        return [self._methodName]

    def applyMethod(self, methodName):
        if methodName != self._methodName:
            return

        # Nutzt die Methode der Basisklasse
        allCurves = self.getAllCurves()
        
        if not allCurves or len(allCurves) < 2:
            if self.plotWindow:
                qt.QMessageBox.information(self.plotWindow, "Info", 
                                         "Bitte laden Sie mindestens zwei Kurven.")
            return

        groups = {}
        for x, y, legend, info in allCurves:
            # Überspringe bereits berechnete Averages
            if "_avg" in legend:
                continue
                
            # Gruppierung nach ROI/Counter
            roi_name = info.get('ylabel', 'Unknown ROI')
            if roi_name not in groups:
                groups[roi_name] = []
            groups[roi_name].append((x, y, legend))

        for roi_name, curves in groups.items():
            if len(curves) < 2:
                continue

            try:
                # Annahme: X-Achsen sind identisch (Scan-Wiederholung)
                y_stack = np.array([c[1] for c in curves])
                x_data = curves[0][0]
                
                avg_y = np.mean(y_stack, axis=0)
                std_y = np.std(y_stack, axis=0, ddof=1)
                
                # Dynamische Legende, um Überschreiben zu verhindern (optional)
                # Hier kannst du z.B. einen Counter oder Zeitstempel einbauen
                new_legend = f"{roi_name}_avg"
                
                # Kurve mit sigmay hinzufügen
                self.addCurve(x_data, avg_y, 
                            legend=new_legend, 
                            info={'ylabel': roi_name},
                            sigmay=std_y,
                            replace=False)

                # self.addCurve(x_data, avg_y + std_y, legend=f"{new_legend}_std_up", linestyle=':', replace=False)
                # Zeichne untere Grenze
                # self.addCurve(x_data, avg_y - std_y, legend=f"{new_legend}_std_down", linestyle=':', replace=False)
                                
            except Exception as e:
                print(f"Fehler bei ROI {roi_name}: {str(e)}")

        # Sicherer Replot
        if self.plotWindow:
            self.plotWindow.replot()

def getPlugin1DInstance(plotWindow, **kw):
    return DataStatsPlugin(plotWindow, **kw)