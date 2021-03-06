from django.db import models
from decimal import *

class FundraisingGoal(models.Model):
    """Conservancy fundraiser Goal"""

    fundraiser_code_name      = models.CharField(max_length=200, blank=False, unique=True)
    fundraiser_goal_amount   = models.DecimalField(max_digits=10, decimal_places=2)
    fundraiser_so_far_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fundraiser_donation_count = models.IntegerField()
    fundraiser_donation_count_disclose_threshold = models.IntegerField()

    def __unicode__(self):
        return self.fundraiser_code_name

    def percentage_there(self):
        return (self.fundraiser_so_far_amount / self.fundraiser_goal_amount ) * Decimal('100.00')
    
    class Meta:
        ordering = ('fundraiser_code_name',)
