from app.intelligence.maintenance_analyzer import MaintenanceAnalyzer


class RiskEngine:

    @staticmethod
    def calculate(

        db,

        equipment_id,

    ):

        failures = (

            MaintenanceAnalyzer.count_failures(

                db,

                equipment_id,

            )

        )

        if failures >= 10:

            return "Critical"

        if failures >= 5:

            return "High"

        if failures >= 3:

            return "Medium"

        return "Low"