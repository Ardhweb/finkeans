from django.urls import path
from . import views
app_name = 'club'  # Define the app's namespace here
urlpatterns = [
    path('create-new-record/', views.create_new_record, name='create_new_record'),
    path('add_column_head_form/', views.add_column_head_form, name='add_column_head_form'),
    path('success-record-column/', views.success_record_col, name="success_record_column"),
    path('club-dashboard/', views.club_dashboard, name="club_dashboard"),
    path('<int:id>/insert-databook/', views.insert_databook, name="insert_databook"),
    path('<int:id>/view-databook/', views.view_databook, name="view_databook"),
    
]
