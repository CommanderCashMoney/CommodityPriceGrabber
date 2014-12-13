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

##################################
#screen res adjustment
#s = Screen(0)
#xAd = 0.625
#yAd = 0.817
#################################################################
class GrabPrices:
# switch to ED and grab prices
    
    def __init__(self):
        
        App.focus("Elite - Dangerous (CLIENT)")
        #find commodity header
        global header
        header = find("1416765457866-2.png")
       
        #define working grid where we will look for rows. 
        #This limits the search area if you are running multiple monitors and speeds up the search
        grid = Region(header.x - 13, header.y,100,840)
        #capture(grid)
        #global station
        #stationpic = capture(Region(header.x - 10, header.y - 150, 500,50))
        #station = self.enlargeimage(stationpic,300, -1)
        #print station.text()
        global arr
        arr = []

        for x in range(70):
            p = Pattern("1418504363339.png")
            rowstart = grid.find(p)
          
            #capture images
            namepic = capture(Region(rowstart.x + 20, rowstart.y + 3, 300,30))
            name = Region(rowstart.x + 20, rowstart.y + 3, 300,30).text()
            sellpic = capture(Region(rowstart.x + 370, rowstart.y + 3,100,30))
            buypic = capture(Region(rowstart.x + 462, rowstart.y + 3,100,30))
            supplypic = capture(Region(rowstart.x + 820, rowstart.y + 3,200,30))
            galavgpic = capture(Region(rowstart.x + 1030, rowstart.y + 3,170,30))
            #exit loop when the exit button is found
            if name.find("EXIT") >= 0:
                break
           
            #arr.append([name,namepic,sellprice,sellpic,buyprice,buypic,supply,alert,supplypic])
            arr.append([namepic,sellpic,buypic,supplypic,galavgpic])
            
            #wait(0.2)
            keyDown("s")
            wait(0.1)
            keyUp("s")
            wait(0.25)
class extractPrices:
    timestried = 0
    def __init__(self):
        global arr2
        arr2 = []
        for row in arr:
            name = self.enlargeimage(arr[arr.index(row)][0],400, -1)
            sellprice = self.enlargeimage(arr[arr.index(row)][1],110,40)
            buyprice = self.enlargeimage(arr[arr.index(row)][2],110,40)
            supply = self.enlargeimage(arr[arr.index(row)][3],220,45)
            galavg = self.enlargeimage(arr[arr.index(row)][4],185,42)
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
            name = str(re.sub("[^a-zA-Z\.\- ]","",name))
            namecleaned, namefound = nameclean.NameCleaner().cleanNames(name)
            if namefound == 0:
                alert = alert + "namewarning"
            arr2.append([namecleaned,arr[arr.index(row)][0],sellprice,arr[arr.index(row)][1],buyprice,arr[arr.index(row)][2],supply,alert,arr[arr.index(row)][3]])
            #arr2.append([name,sellprice,buyprice,supply,alert])
   
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
        try: 
            ImageIO.write(bImage, "png", outputfile)
            return re.sub("[^a-zA-Z0-9\.\- ]","", Image.text(image))
        except:
            print "Image Write failed -  retrying"
            wait(0.1)
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
        #p = swing.JPanel()
        #self.field = swing.JTextField(station, 17)
        #self.field.setFont(awt.Font("Arial", awt.Font.BOLD, 30))
        #self.field.setName("textfieldStation")
         
        #p.add(self.field)
        #self.resultPanel.add(p)
        #loop through items and create panels
        for row in arr2:
            #name
            p = swing.JPanel()
            p.add(swing.JLabel(swing.ImageIcon(arr2[arr2.index(row)][1],"East")))
            self.field = swing.JTextField(str(arr2[arr2.index(row)][0]), 17)
            self.field.setFont(awt.Font("Arial", awt.Font.BOLD, 30))
            self.field.setName("textfieldName")
            p.add(self.field)
            if (str(arr2[arr2.index(row)][7])).find('namewarning') > 0:
               self.field.setBackground(awt.Color.red)
            self.resultPanel.add(p)
            #sell price
            p = swing.JPanel()
            p.add(swing.JLabel(swing.ImageIcon(arr2[arr2.index(row)][3],"East")))
            self.field = swing.JTextField(str(arr2[arr2.index(row)][2]), 7)
            self.field.setFont(awt.Font("Arial", awt.Font.BOLD, 30))
            self.field.setName("textfield")
            p.add(self.field)
            if (str(arr2[arr2.index(row)][7])).find('sellwarning') > 0:
               self.field.setBackground(awt.Color.red)
            
            self.resultPanel.add(p)
            #buy price
            if arr2[arr2.index(row)][4] != 0 | arr2[arr2.index(row)][6] != 0:
                p = swing.JPanel()
                p.add(swing.JLabel(swing.ImageIcon(arr2[arr2.index(row)][5],"East")))
                self.field = swing.JTextField(str(arr2[arr2.index(row)][4]), 7)
                self.field.setFont(awt.Font("Arial", awt.Font.BOLD, 30))
                self.field.setName("textfield")
                p.add(self.field)
                if (str(arr2[arr2.index(row)][7])).find('buywarning') > 0:
                   self.field.setBackground(awt.Color.red)
            
                self.resultPanel.add(p)  
            #supply.. only shows if buy price is not 0 and supply price is 0
            if arr2[arr2.index(row)][4] != 0: 
                if arr2[arr2.index(row)][6] == 0:
                    p = swing.JPanel()
                    p.add(swing.JLabel(swing.ImageIcon(arr2[arr2.index(row)][8],"East")))
                    self.field = swing.JTextField(str(arr2[arr2.index(row)][6]), 7)
                    self.field.setFont(awt.Font("Arial", awt.Font.BOLD, 30))
                    self.field.setName("textfield")
                    p.add(self.field)
                    if (str(arr2[arr2.index(row)][7])).find('supplywarning') > 0:
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
                #if (fields.getName() == 'textfieldStation'):
                #    global stationtext
                #    stationtext = fields.text
                   
                    
                if  (fields.getName() == 'textfieldName'):
                    rowcounter = rowcounter + 1
                    colcounter = 0
                if (fields.getName() == 'textfield') | (fields.getName() == 'textfieldName'):
                   
                    arr2[rowcounter][colcounter] = fields.text
                    #print fields.text
                    
                    colcounter = colcounter + 2
        Thread(target=lambda: sendtoSlopey()).start()
       
        
class sendtoSlopey(Runnable):        
    def __init__(self):               
        App.focus("ED BEST")
        click("1418344169076-1.png")
        type(Key.TAB)
        #type(stationtext[:4])
        type(Key.TAB)
        for row in arr2:
            namecleaned, namefound = nameclean.NameCleaner().cleanNames(str(arr2[arr2.index(row)][0]))
            if namefound == 1:
                
                type(str(arr2[arr2.index(row)][0]))
                type(Key.TAB)
                type(str(arr2[arr2.index(row)][2]))
                type(Key.TAB)
                type(str(arr2[arr2.index(row)][4]))
                type(Key.TAB)
                type(str(arr2[arr2.index(row)][6]))
                type(Key.TAB)
                type(Key.ENTER)          

GrabPrices()
extractPrices()
PriceVerify()





            
