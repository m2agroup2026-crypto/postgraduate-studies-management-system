from django.core.management.base import BaseCommand

from apps.data_migration.services.excel_reader import ExcelReader


class Command(BaseCommand):
    help = "Analyze legacy Excel file structure"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=str,
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]

        reader = ExcelReader(file_path)

        result = reader.inspect()

        self.stdout.write(
            self.style.SUCCESS(
                f"File: {result['file_name']}"
            )
        )

        self.stdout.write(
            f"Sheets: {result['sheet_count']}"
        )

        for sheet in result["sheets"]:
            self.stdout.write("")
            self.stdout.write(
                f"Sheet: {sheet['name']}"
            )
            self.stdout.write(
                f"Rows: {sheet['rows']}"
            )
            self.stdout.write(
                f"Columns: {sheet['columns']}"
            )
