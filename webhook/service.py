import httpx
from datetime import datetime
import asyncio
from webhook.models import Message


class WhatsapSevice():
    BASE_URL="https://graph.facebook.com/v14.0/551602171364742/messages"
    ACCESS_TOKEN="EAAPp0EdFjMYBO3KeqWp37Jw4swtzHcZAfMRWXjtOOlbDUm6JNX6rc7ONKFcxu7wcrldDjMXEej2y7bL0BLJUxtGYwgO0e5vZAXy5hA3ZCFhB3f6pFJM8Ek7Ejz5PmOfTcoLRTOTZCuWTxBDzxj4co5Ep1rGOEwghtyAOlGKak1XUsiwmp9qFT6ZBumpHrPeJAah3DX70kRaggrv31pZBQ78kvsWiUZD"
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
            

