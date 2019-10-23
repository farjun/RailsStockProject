from myapp import stock_api
from myapp.models import Notification
import time


class Notifications:
    
    
    def save_notification(stock_symbol, message):

        notification = Notification()
        notification.stock_id = stock_symbol
        notification.message = message
        notification.read = False
        notification.save()

        
    def check_stock_price():
        #testing notification system 
        while True:

            data = stock_api.get_stock_info('MU')
            latest_price = int(data['latestPrice'])
            previous_close = int(data['previousClose'])

            difference = round(abs(((previous_close - latest_price)  / previous_close) * 100), 2)
            
            if previous_close > latest_price:
                message = "MU Stock's price decrease by "+str(difference)+" %"
                Notifications.save_notification('MU',message)

            elif previous_close < latest_price:
                message = "MU Stock's price increased by "+str(difference)+" %"
                Notifications.save_notification('MU',message)
            
            time.sleep(2)
            
            
        




	
	

	