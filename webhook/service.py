import httpx
from datetime import datetime
import asyncio
from webhook.models import Message


class WhatsapSevice():
    BASE_URL="https://graph.facebook.com/v14.0/551602171364742/messages"
    ACCESS_TOKEN="EAAPp0EdFjMYBO1Q5BkgNWToPIHLTERi4fCz0ecCX7ZCbbyj6EhogOuetnU6W4e0mFKn5Rry2ogNDZBQuy0p4WfOMNVLjcL4SdVlJiYeuZB9Kg6FAEZAkV0n1iL5S1mrmnlO4RVZAdqLa75BWZBFPOpcCjR7YmnzuHhPTaPgZC6kSwJOjOYElsZCpHzSZAjSWxeCq2K2Uhs4PwMzK69EtnykDAPFlEREw2"
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
                if respone.status_code==200:
                    return True,respone.json()
                else:
                    return False, respone.json()
        except Exception as e:
            return False,{"error":str(e)}
            

