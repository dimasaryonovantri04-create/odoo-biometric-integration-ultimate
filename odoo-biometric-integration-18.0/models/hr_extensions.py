from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def api_process_attendance(self, secret_key, attendances):
        """API Endpoint to receive raw attendance data and process it in real-time."""
        conf_key = self.env['ir.config_parameter'].sudo().get_param('hr_biometric_integration.secret_key')
        if not conf_key or secret_key != conf_key:
            raise ValidationError("Secret Key is not valid.")

        if not isinstance(attendances, list):
            raise UserError("Attendances data must be a list of dictionaries.")

        BiometricData = self.env['hr.biometric.data']
        logs_to_create = []
        
        for att_data in attendances:
            employee = self.env['hr.employee'].search([('barcode', '=', att_data.get('uid'))], limit=1)
            if not employee:
                continue 

            try:
                timestamp_str = att_data.get('timestamp')
                # Konversi ke UTC berdasarkan Timezone di Setting
                timezone_str = self.env['ir.config_parameter'].sudo().get_param('hr_biometric_integration.biometric_timezone', 'UTC')
                SOURCE_TIMEZONE = pytz.timezone(timezone_str)
                naive_dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                aware_local_dt = SOURCE_TIMEZONE.localize(naive_dt, is_dst=None)
                utc_dt = aware_local_dt.astimezone(pytz.utc)
                timestamp_for_odoo = fields.Datetime.to_string(utc_dt)
            except Exception:
                continue

            logs_to_create.append({
                'employee_id': employee.id,
                'employee_barcode': att_data.get('uid'),
                'timestamp': timestamp_for_odoo,
                'status': 'pending',
            })
        
        if logs_to_create:
            created_logs = BiometricData.create(logs_to_create)
            # Ini yang membuatnya REAL-TIME
            created_logs.action_process_logs()

        return {
            'status': 'success',
            'summary': f"{len(logs_to_create)} attendance pings logged and processed."
        }

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    biometric_data_ids = fields.One2many(
        'hr.biometric.data', 'attendance_id',
        string='Biometric Raw Data',
        readonly=True,
        help="Raw data logs from the biometric device that generated this attendance record."
    )
