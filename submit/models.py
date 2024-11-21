from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import requests
from io import BytesIO
from django.core.files.base import ContentFile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image.name != 'avatar.jpg':
            try:
                response = requests.get(self.image.url)
                img = Image.open(BytesIO(response.content))

                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)

                    img_io = BytesIO()
                    img.save(img_io, format=img.format)
                    
                    self.image.save(self.image.name, ContentFile(img_io.getvalue()), save=False)

            except Exception as e:
                print(f"Error processing image: {e}")

        super().save(*args, **kwargs)

    

