from django.contrib import admin
from django.urls import path, include
from .views import (home_view, login_view, welcome_view, trace_detail_view, warehouse_view, warehouse_ajax_view, update_duration_view,
start_end_traceability_ajax_view, logout_view, check_traceability_start_view, production_qc_view, report_view, html_report_view)
app_name='traceability'

urlpatterns = [
    path('',home_view,name='home-view'),
    path('login',login_view, name='login-view'),
    path('welcome',welcome_view, name='welcome-view'),
    path('trace_detail/<int:id>', trace_detail_view, name='trace-detail-view'),
    path('warehouse/<int:id>',warehouse_view, name='warehouse-view'),
    path('warehouse/<int:id>/warehouse_ajax', warehouse_ajax_view, name='warehouse-ajax-view'),
    path('update_duration/<int:id>',update_duration_view, name='update-duration-view'),
    path ('start_traceability', start_end_traceability_ajax_view, name = 'start-end-traceability-ajax-view'),
    path('logout', logout_view, name='logout-view'),
    path('check_traceability_start_view/<int:id>', check_traceability_start_view, name = 'check-traceability-start-view'),
    path('production_qc/<int:id>',production_qc_view, name = 'production-qc-view'),
    path('report/<int:id>',report_view, name = 'report-view'),
    path('html_report/<int:id>',html_report_view, name = 'html-report-view')
]
