import json

from django.core.management.base import BaseCommand, CommandError

from apps.data_migration.services.student_importer import StudentWorkbookImporter


class Command(BaseCommand):
    help = "Validate or import the audited legacy student workbook"

    def add_arguments(self, parser):
        parser.add_argument("--source", required=True, help="Path to the source XLSX workbook")
        parser.add_argument("--sheet", help="Worksheet name; defaults to the known source sheet")
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Write accepted rows. Without this flag the command is a dry-run.",
        )

    def handle(self, *args, **options):
        try:
            result = StudentWorkbookImporter(
                source=options["source"],
                sheet_name=options.get("sheet"),
            ).run(commit=options["commit"])
        except (FileNotFoundError, ValueError) as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        if result["failed"]:
            self.stdout.write(
                self.style.WARNING(
                    f"{result['failed']} rows require review; no source data was discarded"
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS("All source rows reconciled"))
