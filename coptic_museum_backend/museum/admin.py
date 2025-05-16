from django.contrib import admin
# from .models import User, Artifact, Event, AIChatbotLog

# class ArtifactAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'historical_period', 'location')
#     search_fields = ('name', 'historical_period')
#     list_filter = ('historical_period', 'location')

# class EventAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'date', 'location')
#     search_fields = ('title', 'location')

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email', 'role')
#     search_fields = ('username', 'email')
#     list_filter = ('role',)



# # Register models to be editable in Django Admin
# admin.site.register(User)
# admin.site.register(Artifact)
# admin.site.register(Event)
# admin.site.register(AIChatbotLog)

from .models import (
    User, Artifact, Event, EventBooking, Notification,
    AIChatbotLog, ChatLog, Hall, InteractiveMap,
    Artifact3DModel, Program
)

admin.site.register(User)
admin.site.register(Hall)
admin.site.register(Artifact)
admin.site.register(Event)
admin.site.register(EventBooking)
admin.site.register(Notification)
admin.site.register(AIChatbotLog)
admin.site.register(ChatLog)
admin.site.register(InteractiveMap)
admin.site.register(Artifact3DModel)
admin.site.register(Program)
