from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
import json
from datetime import datetime
import logging
import os
import asyncio
from django.shortcuts import render,redirect
from rest_framework.response import Response
from webhook.models import Message
from webhook.service import WhatsapSevice
from rest_framework.decorators import api_view
# Create your views here.

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






VERIFY_TOKEN="get_verify"

@csrf_exempt
async def webhook(request):
    if request.method=="GET":
        verify_token=request.GET.get("hub.verify_token")
        challenge=request.GET.get("hub.challenge")
        try:

            if VERIFY_TOKEN==verify_token:
                logger.info(f"User verified successfully")
                return HttpResponse(challenge)

            else:
                logger.error(f"Faild to verification")

                return HttpResponse("verification faild",status=403)
        except Exception as e:
            logger.exception(f"Failded to verification at {str(e)}")

            return JsonResponse({"status":"error","message":str(e)})
        
    elif request.method=="POST":
        try:
            data=json.loads(request.body.decode("utf-8"))


            for entry in data.get('entry', []):
                for change in entry.get('changes', []):
                    messages = change['value'].get('messages', [])
                    for msg in messages:
                        sender = msg.get('from')  # Sender's phone number
                        message_body = msg.get('text', {}).get('body')  # Message content
                        timestamp = msg.get('timestamp')  # Message timestamp (UNIX)

                        dt_object = datetime.utcfromtimestamp(int(timestamp))  # Convert to datetime
                        logger.info(f"got data with this mobile no {sender} at {dt_object}")
                        exists=await asyncio.to_thread(
                                    Message.objects.filter(mobile_no=sender).exists
                                )
                        if exists:
                            await asyncio.to_thread(
                                Message.objects.create,
                                    sender="Rutvik",
                                    receiver=sender,
                                    content=message_body,
                                    timestamp=dt_object,
                                    status="Received",
                                    mobile_no=None
                                        )
                        else:
                            await asyncio.to_thread(
                                Message.objects.create,
                                    sender="Rutvik",
                                    receiver=sender,
                                    content=message_body,
                                    timestamp=dt_object,
                                    status="Received",
                                    mobile_no=sender
                                        )
            
                        
            return JsonResponse({"status":"sucess","message":"Received message"})
        except Exception as e:
            logger.exception(F"received error:{str(e)}")
            return JsonResponse({"status":"sucess","message":str(e)})
                        

@csrf_exempt
async def reply_to_user(request):
    mobile_list=request.POST.getlist("mobile")
    message=request.POST.get("msg")

    if not mobile_list or not message:
        return Response({"status":"error","message":"Mobile no and message are required"},status=400)
    logger.info(f"received send data with mobile list {mobile_list} and message {message}")
    whatsapp_service=WhatsapSevice()
    try:
        task=[]
        for mobile in mobile_list:
            mobile=mobile.strip()
            task.append(whatsapp_service.send_message(mobile,message))

        result=await asyncio.gather(*task)

        for result,mobile_no in zip(result,mobile_list):
            success,data=result

            if not success:
                logger.error(f"faield to send msg ")
                return JsonResponse({"status":"error","mobile no":mobile_no,"message":data})
        return redirect("/")
    except Exception as e:
        logger.exception(f"faield to send message{str(e)}")
        return JsonResponse({"status":"error","message":str(e)})

@api_view(["GET"])
def admin_interface(request):
    data=Message.objects.all()
    msg=[]
    mobile_list=[]

    for message in data:
        msg1={
            "sender":message.sender,
            "receiver":message.receiver,
            "content":message.content,
            "timestamp":message.timestamp,
            "status":message.status
        }
        msg.append(msg1)

        if message.mobile_no:
            mobile_dict={"mobile_no":message.mobile_no}
            mobile_list.append(mobile_dict)


    return render(request,"admin_interface.html",{"messages":msg,"mobile_list":mobile_list})


        






