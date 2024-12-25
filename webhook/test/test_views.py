import os
from django.conf import settings
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE","whatsapp_webhook.settings")

django.setup()

import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient



@pytest.fixture
def client():
    return APIClient()




@pytest.fixture
def test_data():
    return {


    }


def test_for_verification(client):
    url=reverse("webhook")

    response=client.get(url,format="json")
    assert response.status_code==status.HTTP_403_FORBIDDEN

@pytest.fixture
def valid_data():
    return {'object': 'whatsapp_business_account', 'entry': [{'id': '457525804121298', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15551828990', 'phone_number_id': '551602171364742'}, 'contacts': [{'profile': {'name': 'Rutvik Jadhav'}, 'wa_id': '918265057464'}], 'messages': [{'from': '918265057464', 'id': 'wamid.HBgMOTE4MjY1MDU3NDY0FQIAEhggREFBMUNDMTAxQjc4ODE1QzhBQkZGOUU4MTJCRjI3QkYA', 'timestamp': '1735129932', 'text': {'body': 'Hello from jadhav'}, 'type': 'text'}]}, 'field': 'messages'}]}]}


def test_for_receiver_msg(client,valid_data):
    url=reverse("webhook")
    response=client.post(url,valid_data,format="json")
    assert response.status_code==status.HTTP_200_OK


@pytest.fixture
def valid_data_for_send_msg():
    return {
        "mobile":["918265057464","9193220 15008"],
        "msg":"Hello Friend"
    }

def test_for_send_msg(client,valid_data_for_send_msg):
    url=reverse("reply_to_user")
    response=client.post(url,valid_data_for_send_msg,format="multipart")
    assert response.status_code==status.HTTP_302_FOUND


def test_for_admin_interface(client):
    url=reverse("")
    response=client.get(url)
    assert response.status_code==status.HTTP_200_OK
    