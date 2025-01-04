# import uuid
from django.db import models
from users.models import Users

class Conversation(models.Model):
    # id = models.UUIDField(
    #     default=uuid.uuid4, unique=True, primary_key=True, editable=False
    # )
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Conversation with {self.user}"
    

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message in conversation {self.conversation}"
    