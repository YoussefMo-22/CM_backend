# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     role = models.CharField(max_length=50, choices=[('visitor', 'Visitor'), ('admin', 'Admin')])

#     class Meta:
#         app_label = 'museum'  # Explicitly set the app label


# class Artifact(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     image = models.ImageField(upload_to='artifacts/', null=True, blank=True)  # Changed to ImageField
#     historical_period = models.CharField(max_length=100)
#     location = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)

# class Event(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     date = models.DateField()
#     location = models.CharField(max_length=255)

# class MapSection(models.Model):
#     section_name = models.CharField(max_length=255)
#     artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, related_name="map_location")
#     x_coordinate = models.FloatField()
#     y_coordinate = models.FloatField()

# class AIChatbotLog(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     query = models.TextField()
#     response = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)


# # models.py
# class ChatLog(models.Model):
#     user_id = models.CharField(max_length=255)
#     user_message = models.TextField()
#     bot_response = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Chat {self.user_id} at {self.timestamp}"


from django.contrib.auth.models import AbstractUser
from django.db import models

# ------------------ User ------------------
class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=[('visitor', 'Visitor'), ('admin', 'Admin')])

    class Meta:
        app_label = 'museum'

# ------------------ Hall ------------------
class Hall(models.Model):
    number = models.PositiveIntegerField(null=True, blank=True)  # Null for Tube and Churches
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Hall {self.number or ''}: {self.name}"

# ------------------ Artifact ------------------
class Artifact(models.Model):
    register_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    historical_period = models.CharField(max_length=100)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, related_name="artifacts")
    image = models.ImageField(upload_to='artifacts/', null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ------------------ Event & Workshop ------------------
class Event(models.Model):
    EVENT_TYPE_CHOICES = [('event', 'Event'), ('workshop', 'Workshop')]
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.title} ({self.type})"

class EventBooking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"

# ------------------ Notification ------------------
class Notification(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for: {self.event.title}"

# ------------------ Chat Logs ------------------
class AIChatbotLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ChatLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# ------------------ Interactive Map ------------------
class InteractiveMap(models.Model):
    hall = models.OneToOneField(Hall, on_delete=models.CASCADE, related_name="map")
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()

# ------------------ 3D Model ------------------
class Artifact3DModel(models.Model):
    artifact = models.OneToOneField(Artifact, on_delete=models.CASCADE, related_name='model3d')
    model_file = models.FileField(upload_to='3d_models/')
    description = models.TextField(blank=True, null=True)

# ------------------ Programs (Suggested Tours) ------------------
class Program(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    artifacts = models.ManyToManyField(Artifact)

    def __str__(self):
        return self.title
