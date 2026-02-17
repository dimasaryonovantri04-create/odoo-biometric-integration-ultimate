from odoo import fields, models
import pytz

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    biometric_secret_key = fields.Char(
        string='Biometric Secret Key',
        config_parameter='hr_biometric_integration.secret_key',
    )
    
    biometric_timezone = fields.Selection(
        selection=[(tz, tz) for tz in pytz.all_timezones],
        string='Biometric Device Timezone',
        config_parameter='hr_biometric_integration.biometric_timezone',
        help="Penting! Pilih zona waktu yang sesuai dengan lokasi fisik mesin biometrik Anda."
    )
