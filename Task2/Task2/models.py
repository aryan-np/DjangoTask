from django.db import models

# todo list model
class TodoModel(models.Model):
    # setup model's field 
    title = models.CharField(max_length=100,null=False,blank=False)
    description = models.CharField(max_length=1000)
    completed = models.BooleanField(default=False)
    # owner= models.ForeignKey()
    
    def __str__(self):
        return self.title