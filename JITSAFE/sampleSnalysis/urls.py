from django.urls import path
from rest_framework.urls import app_name

from sampleSnalysis.views import UploadExcelView, GetFilesView, DeleteFileView, AnalysisModelView, ChangeRemarksView, \
    HistoryModelView

app_name = 'sampleSnalysis'
urlpatterns = [
    path('upload',UploadExcelView.as_view(),name='upload'),
    path('get_data',GetFilesView.as_view(),name='get_data'),
    path('delete',DeleteFileView.as_view(),name='delete'),
    path('analyse',AnalysisModelView.as_view(),name='analyse'),
    path('update/remark',ChangeRemarksView.as_view(),name='change_remarks'),
    path('get/history',HistoryModelView.as_view(),name='history')
]