from django.db import models
# Create your models here.
from datetime import datetime



class Inbox(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    channel_type = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Inboxes"
    

class Agent(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    available_name = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Agents"
    

class Contacts(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100 , null=True , blank=True)
    phone = models.CharField(max_length=100 , null=True , blank=True)
    email = models.EmailField(null=True , blank=True)
    city = models.CharField(max_length=100 , null=True , blank=True)
    country = models.CharField(max_length=100 , null=True , blank=True)
    inbox = models.ForeignKey(Inbox, on_delete=models.SET_NULL, null=True, related_name="inboxes")
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name_plural = "Contacts"

class Conversation(models.Model):
    contact = models.ForeignKey(Contacts, on_delete=models.SET_NULL, null=True, related_name="conversations")
    channel = models.CharField(max_length=200, null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, related_name="agent_conversations")
    id = models.IntegerField(primary_key=True)
    inbox = models.ForeignKey(Inbox, on_delete=models.SET_NULL, null=True, related_name="inbox_conversations")
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name_plural = "Conversations"


    