# from django.contrib import admin
# # from .models import User, Artifact, Event, AIChatbotLog

# # class ArtifactAdmin(admin.ModelAdmin):
# #     list_display = ('id', 'name', 'historical_period', 'location')
# #     search_fields = ('name', 'historical_period')
# #     list_filter = ('historical_period', 'location')

# # class EventAdmin(admin.ModelAdmin):
# #     list_display = ('id', 'title', 'date', 'location')
# #     search_fields = ('title', 'location')

# # class UserAdmin(admin.ModelAdmin):
# #     list_display = ('id', 'username', 'email', 'role')
# #     search_fields = ('username', 'email')
# #     list_filter = ('role',)



# # # Register models to be editable in Django Admin
# # admin.site.register(User)
# # admin.site.register(Artifact)
# # admin.site.register(Event)
# # admin.site.register(AIChatbotLog)

# from .models import (
#     User, Artifact, Event, EventBooking, Notification,
#     AIChatbotLog, ChatLog, Hall, InteractiveMap,
#     Artifact3DModel, Program
# )

# admin.site.register(User)
# admin.site.register(Hall)
# admin.site.register(Artifact)
# admin.site.register(Event)
# admin.site.register(EventBooking)
# admin.site.register(Notification)
# admin.site.register(AIChatbotLog)
# admin.site.register(ChatLog)
# admin.site.register(InteractiveMap)
# admin.site.register(Artifact3DModel)
# admin.site.register(Program)

from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import (
    User, Hall, Artifact, Event, EventBooking,
    Notification, AIChatbotLog, ChatLog,
    InteractiveMap, Artifact3DModel, Program
)

# ----- User -----
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_staff', 'is_active')

# ----- Hall -----
@admin.register(Hall)
class HallAdmin(TranslatableAdmin):
    list_display = ('number', 'name')
    search_fields = ('translations__name',)

# ----- Artifact -----
@admin.register(Artifact)
class ArtifactAdmin(TranslatableAdmin):
    list_display = ('register_number', 'hall', 'name', 'created_at')
    search_fields = ('register_number', 'translations__name', 'translations__historical_period')
    list_filter = ('hall',)

# ----- Event -----
@admin.register(Event)
class EventAdmin(TranslatableAdmin):
    list_display = ('date', 'type', 'title')
    search_fields = ('translations__title',)
    list_filter = ('type', 'date')

# ----- EventBooking -----
@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event')
    search_fields = ('user__username', 'event__translations__title')
    list_filter = ('event',)

# ----- Notification -----
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('event', 'created_at')
    search_fields = ('event__translations__title',)
    list_filter = ('created_at',)

# ----- AIChatbotLog -----
@admin.register(AIChatbotLog)
class AIChatbotLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'created_at')
    search_fields = ('user__username', 'query')
    list_filter = ('created_at',)

# ----- ChatLog -----
@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp')
    search_fields = ('user__username', 'user_message', 'bot_response')
    list_filter = ('timestamp',)

# ----- InteractiveMap -----
@admin.register(InteractiveMap)
class InteractiveMapAdmin(admin.ModelAdmin):
    list_display = ('hall', 'x_coordinate', 'y_coordinate')
    search_fields = ('hall__translations__name',)

# ----- Artifact3DModel -----
@admin.register(Artifact3DModel)
class Artifact3DModelAdmin(admin.ModelAdmin):
    list_display = ('artifact',)
    search_fields = ('artifact__translations__name',)

# ----- Program -----
@admin.register(Program)
class ProgramAdmin(TranslatableAdmin):
    list_display = ('title',)
    search_fields = ('translations__title',)
