from __future__ import division
class PriceVerify:
    def _init_():
        verify()
    def verify(self,sellprice,buyprice,supply,galavg,name):
        alert = "-"
        if buyprice == 0:
            if supply != 0:
                print("PRICE ALERT: Buy price is zero yet there is a supply of " + name)
                alert = "buywarning"
        if buyprice != 0:
            buyselldiff = 100-((sellprice/buyprice) * 100)
            if buyselldiff > 40:
                print("PRICE ALERT: " + str(buyselldiff) + "% increase from Buy price on " + name)
                alert = "sellwarning"
            if buyselldiff < -40:
                print("PRICE ALERT: " + str(buyselldiff) + "% decrease from Buy price on " + name)
                alert = "sellwarning"
            if galavg != 0:
                buyavgdiff = 100-((buyprice/galavg) * 100)
                if buyavgdiff > 75:
                    print("PRICE ALERT: Buy price is " + str(buyavgdiff) + "% increase from Galactic Average price on " + name)
                    alert = "buywarning"
                if buyavgdiff < -75:
                    print("PRICE ALERT: Buy price is " + str(buyavgdiff) + "% decrease from Galactic Average price on " + name)
                    alert = "buywarning"
            if sellprice > buyprice:
                print("PRICE ALERT: Sell price is higher than Buy price on " + name)
                alert = "sellwarning"
            if supply == 0:
                print("PRICE ALERT: Supply number can not be zero if a buy price is listed " + name)
                alert = "supplywarning"

        if sellprice == 0:
            print("PRICE ALERT: Sell Price is set to zero for: " + name)
            alert = "sellwarning"
        if len(name) < 3:
            print("INVALID NAME: " + name)
            alert = "namewarning"
            
        if galavg != 0:
            sellavgdiff = (100-((sellprice/galavg) * 100))
                     
            if sellavgdiff > 75:
                    print("PRICE ALERT: Sell price is " + str(sellavgdiff) + "% increase from Galactic Average price on " + name)
                    alert = "sellwarning"
            if sellavgdiff < -75:
                    print("PRICE ALERT: Sell price is" + str(sellavgdiff) + "% decrease from Galactic Average price on " + name)
                    alert = "sellwarning"
        return alert
