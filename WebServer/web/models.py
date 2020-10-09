from django.db import models

# Create your models here.

class Extension(models.Model):
    extension_name = models.CharField(max_length=100)
    icon_name = models.CharField(max_length=100, default="nonpic.png")
    displayed = models.BooleanField(default=True)

    def __str__(self):
        return "{}: {}".format(self.id, self.extension_name)

    @property
    def has_highscores(self):
        saved_data = SavedData.objects.filter(extension=self, field_name='highscore')
        return saved_data.exists()

class ConfigEntry(models.Model):
    extension = models.ForeignKey(Extension, on_delete=models.CASCADE)
    config_key = models.CharField(max_length=100)
    config_value = models.CharField(max_length=100)

    def __str__(self):
        return "[{}] {}: {} -> {}".format(self.id, self.extension.extension_name, self.config_key, self.config_value)

class SavedData(models.Model):
    extension = models.ForeignKey(Extension, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return "[{}] {}: {}".format(self.extension.extension_name, self.field_name, self.content)