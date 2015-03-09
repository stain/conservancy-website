from django.db import models

class FundraisingGoal(models.Model):
    """Conservancy fundraiser Goal"""

    fundraiser_code_name      = models.CharField(max_length=200, blank=False, unique=True)
    fundraiser_goal_amount   = models.DecimalField(max_digits=10, decimal_places=2)
    fundraiser_so_far_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return self.fundraiser_code_name

    class Meta:
        ordering = ('fundraiser_code_name',)
