from django.core.management.commands.shell import Command as ShellCommand
from tenant_router.managers.task_local import tls_tenant_manager
from tenant_router.managers import tenant_context_manager
from tenant_router.managers.tenant_context import TenantContextNotFound
from django.core.management.base import CommandError


class Command(ShellCommand):
    help = "Starts the Python interactive interpreter bound to a tenant."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "tenant_id", help="Tenant ID to bind the shell to (required)."
        )

    def handle(self, *args, **options):
        tenant_id = options.get("tenant_id")
        try:
            tenant_ctx = tenant_context_manager.get_by_id(tenant_id)
            if not tenant_ctx:
                raise TenantContextNotFound
        except TenantContextNotFound:
            raise CommandError(f"Tenant '{tenant_id}' not found.")

        self.stdout.write(self.style.SUCCESS(f"Binding shell to tenant: {tenant_id}"))
        tls_tenant_manager.push_tenant_context(tenant_ctx)

        try:
            super().handle(*args, **options)
        finally:
            tls_tenant_manager.pop_tenant_context()
            self.stdout.write(
                self.style.WARNING(f"Tenant '{tenant_id}' context popped.")
            )
