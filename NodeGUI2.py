
import sys
from   PySide.QtCore import *
from   PySide.QtGui  import *
from   PysideGraph   import *
from   HoverScene    import *
import plotSubWin    as qtplt
import numpy as np




class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.initToolBar()
		self.initDocker()
		self.view  = QGraphicsView()
		self.scene = DiagramScene()
		
		self.scene.setSceneRect(0,0,1920,1920)
		self.setCentralWidget(self.view)
		#Select node connection and its decorator types
		self.nc = CenterCalc()
		self.cd = LineArrowOnStart()          

		root = JackNode(self.scene, self.nc, self.cd,  x =400, y =200, name = 'data')
		root.addSource()
		a = np.array([ i for i in xrange(200)], dtype = float) * np.pi/100
		
		root.output = [a.tolist(), np.sin(a).tolist()]

		plot = JackNode(self.scene, self.nc, self.cd,  x =400, y =200, name = 'plot')
		plot.addPlug()		
		plot.addPlug()
		plot.setScript(self.plot)

		norm = JackNode(self.scene, self.nc, self.cd,  x =400, y =200, name = 'normalize')
		norm.addPlug()		
		norm.addSource()
		norm.setScript(self.Normalize)

		norm2 = JackNode(self.scene, self.nc, self.cd,  x =400, y =200, name = 'normalize')
		norm2.addPlug()		
		norm2.addSource(name = '2234')
		norm2.setScript(self.Normalize)

		self.view.setScene(self.scene)
		self.view.show()

	def initToolBar(self):
		self.toolbar = QToolBar()
		
		self.addToolBar(self.toolbar)
		self.addObjAction = QAction('add', self)
		self.toolbar.addAction(self.addObjAction)
		self.addObjAction.triggered.connect(self.addJackNode)

		self.runScriptAction = QAction('run', self)
		self.toolbar.addAction(self.runScriptAction)
		self.runScriptAction.triggered.connect(self.runScript)

	def initDocker(self):


		self.plotDock        = QDockWidget("Plot View", self)
		self.propertyDock    = QDockWidget("property",  self)

		self.plotDock.setMinimumSize(300,300)
		self.propertyDock.setMinimumSize(300,100)

		self.plotDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
		self.propertyDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
		
		self.addDockWidget(Qt.RightDockWidgetArea, self.plotDock)
		self.addDockWidget(Qt.RightDockWidgetArea, self.propertyDock)

	def plot(self, data1 = [], data2 = []):

		datas      = [data1, data2]
		plotWindow = qtplt.PlotWindow()
		p,l        = plotWindow.addPlotArea('graphtitle')
		colorMap   = [(10,10,10,255),    (255,0,0,255),   (0,0,255,255),  (20,200,0,255),
					  (255,0,115,255),   (190,150,0,255), (10,0,175,255), (140,67,10,255),
					  (255,0,255,255),   (15,110,0,255),  (0,37,102,255), (255,185,0,255),
					  (130,0,217,255),   (85,0,212,255)]  
		for data in datas:
			if data != []:
				[X, Y] = data
				plotWindow.insertPlot(X, Y, plotArea = p, legend = l, lineColor = colorMap[1], dotColor = colorMap[0])
				plotWindow.finitPlotArea(plotArea = p, legend = l)

		

		self.plotDock.setWidget(plotWindow)
		plotWindow.showMaximized()
		return 0   

	def differential(self, array=[[],[]]):
		if array != [[],[]]:
			dx = np.array(array[0][0:-1], dtype=np.float) + np.diff(np.array(array[0], dtype=np.float)/2)
			dy = np.diff(np.array(array[1], dtype=np.float))
			return [dx.tolist(),dy.tolist()]
		return 0

	def Normalize(self, array=[]):
		if array != []:
			Max = max(array[1])
			Min = min(array[1])
			return [array[0], (2 * np.array(array[1]) / abs(Max-Min)).tolist()]
		return 0

	def addJackNode(self):
		root = JackNode(self.scene, self.nc, self.cd,  x =300, y =200 )
		root.addPlug()
		root.addSource()
		root.setScript(self.differential)
		root.setName(u'Diff')
		# root.output = [[1,2,3,4,5,6,7], [2,4,16,256,65536,4294967296,1.844674407e19]]
		

	
	def runScript(self):
		self.scene.runScript()
		


				
				


app = QApplication(sys.argv)
# MainWindow = listItem()
MainWindow = MainWindow()
MainWindow.show()

def load_stylesheet(pyside=True):
	f = QFile("./style.qss")
	if not f.exists():
		return ""
	else:
		f.open(QFile.ReadOnly | QFile.Text)
		ts = QTextStream(f)
		stylesheet = ts.readAll()
		return stylesheet	
app.setStyleSheet(load_stylesheet())
app.exec_()
