from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post

# Create your views here.

BASE_URL = "https://www.deckofcardsapi.com/api/deck/"

class GetCard(APIView):
    def get(self, request, format=None):
        pass