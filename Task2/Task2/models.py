from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

# todo list model
class TodoModel(models.Model):
    # setup model's field 
    title = models.CharField(max_length=100,null=False,blank=False)
    description = models.CharField(max_length=1000)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos',null=True,blank=True)

    
    def __str__(self):
        return self.title