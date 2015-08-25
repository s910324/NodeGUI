
import sys
import numpy         as np
import pyqtgraph     as pg
from   pyqtgraph.Qt  import  QtCore
from   types         import *
from   PySide.QtCore import *
from   PySide.QtGui  import *




class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.mainWindow = QMainWindow()
		self.resize(1000,800)
		self.plotCounter = 0
#        self.initSettingDocker()
		self.initSettingToolbar()
		self.initPlotArea()
		self.plotLineHolder = []

		
	def initSettingToolbar(self):
		self.graphBar = QToolBar('plot options')
		self.addToolBar( Qt.TopToolBarArea , self.graphBar)

		selectAction    = QAction('Select area', self)
		crosshairAction = QAction('Enable CrossHair', self)
		addHLineAction = QAction('Insert Horizontal Line', self)
		addVLineAction = QAction('Insert Verticle Line', self)
		
		self.graphBar.addAction(selectAction)
		self.graphBar.addAction(crosshairAction)
		self.graphBar.addAction(addHLineAction)
		self.graphBar.addAction(addVLineAction)
		#nextAction.triggered.connect(self.test2)    
		
					
		
	def initPlotArea(self):
		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')
		self.view = pg.GraphicsLayoutWidget()         
		scrollBarH = QScrollBar()
		scrollBarV = QScrollBar()
		self.view.setHorizontalScrollBar(scrollBarH)
		self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.view.setVerticalScrollBar(scrollBarV)
		self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.setCentralWidget(self.view)


	
	def addPlotArea(self, graphTitle = ''):
		self.vb = CustomViewBox()
		self.w = self.view.addPlot( viewBox = self.vb, enableMenu = False, title = graphTitle)
		self.view.nextRow()
		self.l = pg.LegendItem((100,60), offset=(70,70))  # args are (size, offset)
		self.l.setParentItem(self.w.graphicsItem())   # Note we do NOT call plt.addItem in this case
		return self.w, self.l
		

	def insertPlot(self, xAry = None, yAry = None, plotArea = None, legend = None, plotName = None, 
				lineColor = (0,0,0,255), lineWidth = 2, lineStyle = QtCore.Qt.SolidLine, 
				dotColor  = (0,0,0,255), dotSize   = 6,  dotSym = 0    ):
			Sym = [ 'o', 's', 't', 'd', '+' ]
			if plotName == None:
				plotName = 'Untitle {0}'.format(self.plotCounter)
				self.plotCounter += 1
			if ( xAry != None and yAry != None):
				line = plotArea.plot( np.array(xAry), np.array(yAry), name = plotName,
								  pen=pg.mkPen(color = lineColor, width=lineWidth, style=lineStyle), symbol = Sym[dotSym] ) 
				self.plotLineHolder.append(line)
			else:
				plotAry = xAry if xAry != None else yAry
				xAry = np.linspace( 0, len( plotAry )-1, len( plotAry ))
				yAry = np.array( plotAry )
				line = plotArea.plot( np.array(xAry), np.array(yAry), name = plotName,
								  pen=pg.mkPen(color = lineColor, width=lineWidth, style=lineStyle), symbol = Sym[dotSym] ) 
				self.plotLineHolder.append(line)
			line.setSymbolBrush( pg.mkBrush(  color = dotColor ))
			line.setSymbolPen(   None )
			line.setSymbolSize( dotSize )
			plotArea.showGrid(x=True, y=True)
			legend.addItem( line, plotName )        


	def finitPlotArea(self, plotArea = None, legend = None, axisNameAry = None, unitAry = None, showAxis = [1, 1, 1, 1]):
		axisNameAry = axisNameAry if type(axisNameAry) == ListType else ['','','','']
		unitAry     = unitAry     if type(unitAry)     == ListType else ['','','','']
		showAxis    = showAxis    if type(showAxis)    == ListType else [ 1, 1, 1, 1]

		for i in range( 0, len(unitAry) - len(axisNameAry)):
			unitAry.append('')
		if len(axisNameAry) > 0:
			plotArea.setLabel(axis = 'bottom', text = axisNameAry[0], units = unitAry[0], unitPrefix = None )
		if len(axisNameAry) > 1:
			plotArea.setLabel(axis = 'left',   text = axisNameAry[1], units = unitAry[1], unitPrefix = None )
		if len(axisNameAry) > 2:
			plotArea.setLabel(axis = 'top',    text = axisNameAry[2], units = unitAry[2], unitPrefix = None )
		if len(axisNameAry) > 3:
			plotArea.setLabel(axis = 'right',  text = axisNameAry[3], units = unitAry[3], unitPrefix = None )
		self.w.showAxis('bottom', show= showAxis[0])
		self.w.showAxis('left',   show= showAxis[1])                
		self.w.showAxis('top',    show= showAxis[2])
		self.w.showAxis('right',  show= showAxis[3])
		
	def modifyPlot(self):
		print 'a'

	  
		
class CustomViewBox(pg.ViewBox):
	def __init__(self, *args, **kwds):
		pg.ViewBox.__init__(self, *args, **kwds)
		self.setMouseMode(self.RectMode)

	def mouseClickEvent(self, ev):
		if ev.button() == QtCore.Qt.RightButton:
			self.autoRange()
			
	def mouseDragEvent(self, ev):
		if ev.button() == QtCore.Qt.RightButton:
			ev.ignore()
		else:
			pg.ViewBox.mouseDragEvent(self, ev)   


if __name__ == '__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()    
	app.exec_()
	sys.exit
