from typing import Dict, Any

class RegionalConfigManager:
    """
    Manages internationalization, currency, timezones, and data privacy 
    policies per region (e.g. EU GDPR vs Brazil LGPD).
    """
    def __init__(self):
        self.regions = {
            "BR": {
                "timezone": "America/Sao_Paulo",
                "language": "pt",
                "currency": "BRL",
                "measurement": "metric",
                "data_policy": "LGPD"
            },
            "UY": {
                "timezone": "America/Montevideo",
                "language": "es",
                "currency": "UYU",
                "measurement": "metric",
                "data_policy": "regional"
            },
            "DE": {
                "timezone": "Europe/Berlin",
                "language": "de",
                "currency": "EUR",
                "measurement": "metric",
                "data_policy": "GDPR"
            }
        }
        
    def get_region_config(self, country_code: str) -> Dict[str, str]:
        if country_code not in self.regions:
            raise ValueError(f"Region {country_code} not configured.")
        return self.regions[country_code]
