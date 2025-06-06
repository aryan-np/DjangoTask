from django.db import models

# todo list model
class TodoModel(models.Model):
    # setup model's field 
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    completed = models.BooleanField(default=False)
    # owner= models.ForeignKey()