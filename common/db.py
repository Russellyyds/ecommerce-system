from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="updated time")
    is_deleted = models.BooleanField(default=False, verbose_name="logically delete")

    class Meta:
        #This is the abstract data model,
        # and when the migration file is executed,
        # no tables are generated in the data
        abstract = True
        verbose_name = "common filed table"
        db_table = 'BaseTable'
