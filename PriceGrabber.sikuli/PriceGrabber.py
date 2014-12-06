from __future__ import division
import javax.swing as swing
from   java.lang      import Runnable;
import java.awt as awt
import java.awt.image
from   javax.swing    import SwingUtilities;
from threading import Thread
from javax.imageio import ImageIO
#import javax.imageio as imageio
from java.io                import File
from java import io
import sys
import re
import nameclean
import priceverify
Settings.OcrTextRead = True
Settings.OcrTextSearch = True

#################################################################
class GrabPrices:
# switch to ED and grab prices
    
    def __init__(self):
    
        App.focus("Elite - Dangerous (CLIENT)")
        #find commodity header
        global header
        header = find("1416765457866-1.png")
       
        #define working grid where we will look for rows. 
        #This limits the search area if you are running multiple monitors and speeds up the search
        grid = Region(header.x - 10, header.y,1200,840)
        global station
        stationpic = capture(Region(header.x - 10, header.y - 150, 500,50))
        station = self.enlargeimage(stationpic,300, -1)
        #print station.text()
        global arr 
        arr = []

        for x in range(70):
            rowstart = grid.find("1416712504495.png")
           
            #capture images
            namepic = capture(Region(rowstart.x + 20, rowstart.y, 300,30))
            name = self.enlargeimage(namepic,400, -1)
 
            #######################
            sellpic = capture(Region(rowstart.x + 370, rowstart.y,100,30))
            sellprice = self.enlargeimage(sellpic,110,40)
                    
            ###################
            buypic = capture(Region(rowstart.x + 462, rowstart.y,100,30))
            buyprice = self.enlargeimage(buypic,110,40)

            ###################
            supplypic = capture(Region(rowstart.x + 820, rowstart.y,200,30))
            supply = self.enlargeimage(supplypic,220,45)

            ########################
            galavgpic = capture(Region(rowstart.x + 1030, rowstart.y,170,30))
            galavg = self.enlargeimage(galavgpic,185,42)

            #exit loop when the exit button is found
            if name.find("EXIT") >= 0:
                break
            #remove any non numbers
            sellprice = re.sub("[^0-9]","",sellprice)
            if sellprice != "":
                sellprice = int(sellprice)
            else:
                sellprice = 0
            buyprice = re.sub("[^0-9]","",buyprice)
            if buyprice != "":
                buyprice = int(buyprice)
            else: 
                buyprice = 0
            supply = re.sub("[^0-9]","",supply)
            if supply != "":
                supply = int(supply)
            else:
                supply = 0
            galavg = re.sub("[^0-9]","",galavg)
            if galavg != "":
                galavg = int(galavg)
            else:
                galavg = 0
            #check price discrepancies
            alert = priceverify.PriceVerify().verify(sellprice,buyprice,supply,galavg,name)
            
            #clean up commodity names
            namecleaned = nameclean.NameCleaner().cleanNames(name)
           
            #clean names of hash tags and only unwanted characters 
            namecleaned =  re.sub("[^a-zA-Z\.\- ]","",namecleaned)
            arr.append([namecleaned,namepic,sellprice,sellpic,buyprice,buypic,supply,alert,supplypic])
           
            
            wait(0.1)
            keyDown("s")
            wait(0.1)
            keyUp("s")
            wait(0.1)
    def enlargeimage(self,image,imagewidth,imageheight):
        imageFile = open(image);
        ###j make image bigger for easier reading
        i = ImageIO.read(imageFile)
        largeimage = i.getScaledInstance(imagewidth, imageheight, awt.Image.SCALE_SMOOTH)
        bImage = awt.image.BufferedImage(largeimage.getWidth(),largeimage.getHeight(),awt.image.BufferedImage.TYPE_INT_ARGB)
        g = bImage.createGraphics()
        g.drawImage(largeimage,0,0,None)
        g.dispose()
        outputfile = File(image)
        ImageIO.write(bImage, "png", outputfile)
 
        return re.sub("[^a-zA-Z0-9\.\- ]","", Image.text(image))
    
                        
#exit()
##########################################################################
class PriceVerify:
    # Display Gui for price verification
    def __init__(self):

        self.frame = swing.JFrame("ED Price Grabber")
        self.frame.setLocation(2600,200)
        self.frame.setLocation(header.x +200, header.y)
        self.resultPanel = swing.JPanel()
    
        scrollpane = swing.JScrollPane(swing.JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,swing.JScrollPane.HORIZONTAL_SCROLLBAR_NEVER)
        scrollpane.preferredSize = 1000, 700
        scrollpane.viewport.view = self.resultPanel
        scrollpane.getVerticalScrollBar().setUnitIncrement(16);
        self.frame.add(scrollpane)

        #Add Station Name
        p = swing.JPanel()
        self.field = swing.JTextField(station, 17)
        self.field.setFont(awt.Font("Arial", awt.Font.BOLD, 30))
        self.field.setName("textfieldStation")
        #todo figure why this field causes screen wrap at reisman settlement in ros 709
        p.add(self.field)
        self.resultPanel.add(p)
        #loop through items and create panels
        for row in arr:
            #name
            p = swing.JPanel()
            p.add(swing.JLabel(swing.ImageIcon(arr[arr.index(row)][1],"East")))
            self.field = swing.JTextField(str(arr[arr.index(row)][0]), 17)
            self.field.setFont(awt.Font("Arial", awt.Font.BOLD, 30))
            self.field.setName("textfieldName")
            p.add(self.field)
            if str(arr[arr.index(row)][7]) == 'namewarning':
               self.field.setBackground(awt.Color.red)
            self.resultPanel.add(p)
            #sell price
            p = swing.JPanel()
            p.add(swing.JLabel(swing.ImageIcon(arr[arr.index(row)][3],"East")))
            self.field = swing.JTextField(str(arr[arr.index(row)][2]), 7)
            self.field.setFont(awt.Font("Arial", awt.Font.BOLD, 30))
            self.field.setName("textfield")
            p.add(self.field)
            if str(arr[arr.index(row)][7]) == 'sellwarning':
               self.field.setBackground(awt.Color.red)
            
            self.resultPanel.add(p)
            #buy price
            if arr[arr.index(row)][4] != 0 | arr[arr.index(row)][6] != 0:
                p = swing.JPanel()
                p.add(swing.JLabel(swing.ImageIcon(arr[arr.index(row)][5],"East")))
                self.field = swing.JTextField(str(arr[arr.index(row)][4]), 7)
                self.field.setFont(awt.Font("Arial", awt.Font.BOLD, 30))
                self.field.setName("textfield")
                p.add(self.field)
                if str(arr[arr.index(row)][7]) == 'buywarning':
                   self.field.setBackground(awt.Color.red)
            
                self.resultPanel.add(p)  
            #supply.. only shows if buy price is not 0 and supply price is 0
            if arr[arr.index(row)][4] != 0: 
                if arr[arr.index(row)][6] == 0:
                    p = swing.JPanel()
                    p.add(swing.JLabel(swing.ImageIcon(arr[arr.index(row)][8],"East")))
                    self.field = swing.JTextField(str(arr[arr.index(row)][6]), 7)
                    self.field.setFont(awt.Font("Arial", awt.Font.BOLD, 30))
                    self.field.setName("textfield")
                    p.add(self.field)
                    if str(arr[arr.index(row)][7]) == 'supplywarning':
                        self.field.setBackground(awt.Color.red)
                    self.resultPanel.add(p)  
            
        mainPanel4 = swing.JPanel()
        mainPanel4.add(swing.JButton("Submit Prices", actionPerformed=self.clickMeCallback), "East")
        
        self.resultPanel.add(mainPanel4)
        panelArray = self.resultPanel.getComponents()
        self.resultPanel.layout = awt.GridLayout(len(panelArray) + 2,3)
        
        self.frame.pack()
        self.frame.show()
        
   
    def clickMeCallback(self, event):
        rowcounter = -1
        colcounter = 0
        panelArray = self.resultPanel.getComponents()
        for panels in panelArray:
            fieldArray = panels.getComponents()
            
            for fields in fieldArray:
                if (fields.getName() == 'textfieldStation'):
                    global stationtext
                    stationtext = fields.text
                   
                    
                if  (fields.getName() == 'textfieldName'):
                    rowcounter = rowcounter + 1
                    colcounter = 0
                if (fields.getName() == 'textfield') | (fields.getName() == 'textfieldName'):
                   
                    arr[rowcounter][colcounter] = fields.text
                    #print fields.text
                    
                    colcounter = colcounter + 2
        Thread(target=lambda: sendtoSlopey()).start()
       
        
class sendtoSlopey(Runnable):        
    def __init__(self):               
        App.focus("ED BEST")
        click("1416780620112.png")
        
        type(stationtext[:4])
        type(Key.TAB)
        for row in arr:
            type(str(arr[arr.index(row)][0]))
            type(Key.TAB)
            type(str(arr[arr.index(row)][2]))
            type(Key.TAB)
            type(str(arr[arr.index(row)][4]))
            type(Key.TAB)
            type(str(arr[arr.index(row)][6]))
            type(Key.TAB)
            type(Key.ENTER)          

GrabPrices()
PriceVerify()





            
