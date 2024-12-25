import httpx
from datetime import datetime
import asyncio
from webhook.models import Message
import logging
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())



# Configure logging to log to a file and console
logger = logging.getLogger(__name__)
 
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

file_handler = logging.FileHandler(f'{log_directory}/app.log')
console_handler = logging.StreamHandler()
 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
 
logger.addHandler(file_handler)
logger.addHandler(console_handler)
 
logger.setLevel(logging.DEBUG)
# This is the token you set up in your Meta Developer Console
VERIFY_TOKEN = "get_verify"  # Replace with your actual token

# Enable logging to inspect incoming requests
logger = logging.getLogger(__name__)

class WhatsapSevice():
    BASE_URL="https://graph.facebook.com/v14.0/551602171364742/messages"
    ACCESS_TOKEN=os.environ["ACCESS_TOKEN"]
    def __init__(self):
        self.headers={
            "Authorization":f"Bearer {self.ACCESS_TOKEN}",
            "Content-Type":"application/json"
        }
    async def send_message(self, mobile_no,message):
        try:
            payload={
                "messaging_product":"whatsapp",
                "to":mobile_no,
                "text":{"body":message}
            }
            async with httpx.AsyncClient() as client:
                respone=await client.post(self.BASE_URL,json=payload,headers=self.headers)
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await asyncio.to_thread(
                                    Message.objects.create,
                                        sender="Rutvik",
                                        receiver=mobile_no,
                                        content=message,
                                        timestamp=timestamp,
                                        status="Sent",
                                            )
                logger.info(f"received mobiel no {mobile_no} and message {message}")
                if respone.status_code==200:
    
                    return True,respone.json()
                else:
                    logger.error(f"failed to send msg")
                    return False, respone.json()
        except Exception as e:
            logger.exception(f"failed to send message{str(e)}")
            return False,{"error":str(e)}
            

