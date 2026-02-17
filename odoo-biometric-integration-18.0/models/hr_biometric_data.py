from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from collections import defaultdict
from datetime import datetime, time
import pytz

class HrBiometricData(models.Model):
    _name = 'hr.biometric.data'
    _description = 'Biometric Raw Attendance Data'
    _order = 'timestamp desc'

    employee_id = fields.Many2one('hr.employee', string='Employee', readonly=True)
    employee_barcode = fields.Char(string="Employee Barcode", readonly=True, index=True)
    timestamp = fields.Datetime(string='Timestamp', readonly=True, required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('error', 'Error'),
    ], string='Status', default='pending', index=True, required=True)
    attendance_id = fields.Many2one('hr.attendance', string='Attendance Record', readonly=True)
    error_message = fields.Text(string='Error Details', readonly=True)

    def action_process_logs(self):
        """Action to be triggered to process pending/error logs."""
        timezone_str = self.env['ir.config_parameter'].sudo().get_param('hr_biometric_integration.biometric_timezone', 'UTC')
        try:
            SOURCE_TIMEZONE = pytz.timezone(timezone_str)
        except pytz.UnknownTimeZoneError:
            raise ValidationError(_("Timezone '%s' is not valid. Please configure it correctly in HR Settings.", timezone_str))
        
        UTC_TIMEZONE = pytz.utc

        daily_scans = defaultdict(lambda: self.env['hr.biometric.data'])
        for log in self:
            if log.employee_id:
                scan_date = log.timestamp.astimezone(SOURCE_TIMEZONE).date()
                key = (log.employee_id.id, scan_date)
                daily_scans[key] |= log
        
        for (employee_id, scan_date), logs in daily_scans.items():
            scans = [log.timestamp for log in logs]
            if not scans:
                continue
            
            first_scan = min(scans)
            last_scan = max(scans)
            
            check_in_utc = first_scan.astimezone(UTC_TIMEZONE)
            check_out_utc = last_scan.astimezone(UTC_TIMEZONE) if len(scans) > 1 else False

            try:
                domain = [
                    ('employee_id', '=', employee_id),
                    ('check_in', '>=', datetime.combine(check_in_utc.date(), time.min)),
                    ('check_in', '<=', datetime.combine(check_in_utc.date(), time.max)),
                ]
                attendance = self.env['hr.attendance'].search(domain, limit=1)

                vals = {
                    'employee_id': employee_id,
                    'check_in': check_in_utc,
                    'biometric_data_ids': [(6, 0, logs.ids)],
                }
                if check_out_utc and check_in_utc != check_out_utc:
                    vals['check_out'] = check_out_utc

                if attendance:
                    attendance.write(vals)
                else:
                    attendance = self.env['hr.attendance'].create(vals)
                
                logs.write({
                    'status': 'processed',
                    'attendance_id': attendance.id,
                    'error_message': False,
                })

            except Exception as e:
                logs.write({'status': 'error', 'error_message': str(e)})

        return True
