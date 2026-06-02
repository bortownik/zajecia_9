import sys

from src.manager import Manager
from src.models import Parameters


def print_section_header(title: str):
    """Print a formatted section header"""


def print_subsection_header(title: str):
    """Print a formatted subsection header"""


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"{amount:,.2f} PLN"


def display_apartments(manager):
    """Display all apartments with their rooms and bills"""
    print_section_header("APARTMENTS")

    for apartment in manager.apartments.values():

        print_subsection_header("Rooms")
        for _room in apartment.rooms.values():
            pass

        # Find bills for this apartment
        apartment_bills = [bill for bill in manager.bills if bill.apartment == apartment.key]
        if apartment_bills:
            print_subsection_header("Bills")
            for _bill in apartment_bills:
                pass


def display_tenants(manager):
    """Display all tenants with their details and transfers"""
    print_section_header("TENANTS")

    for tenant in manager.tenants.values():

        # Find transfers for this tenant
        tenant_transfers = [transfer for transfer in manager.transfers if transfer.tenant == tenant.name]
        if tenant_transfers:
            print_subsection_header("Transfers")
            for _transfer in tenant_transfers:
                pass


def display_monthly_settlement(manager, apartment_key: str, year: int, month: int):
    """Display a full monthly settlement for a given apartment, year and month"""
    if apartment_key not in manager.apartments:
        return

    apartment = manager.apartments[apartment_key]
    settlement = manager.get_settlement(apartment_key, year, month)

    print_section_header(f"MONTHLY SETTLEMENT  —  {apartment.name} ({apartment_key})  |  {month:02d}/{year}")

    # --- Bills ---
    apartment_bills = [
        bill for bill in manager.bills
        if bill.apartment == apartment_key
        and bill.settlement_year == year
        and bill.settlement_month == month
    ]

    print_subsection_header("Bills")
    if apartment_bills:
        for _bill in apartment_bills:
            pass
    else:
        pass

    # --- Per-tenant breakdown ---
    tenant_settlements = manager.create_tenants_settlements(settlement)
    tenants_in_apt = {
        t.name: t for t in manager.tenants.values() if t.apartment == apartment_key
    }

    print_subsection_header("Tenant Breakdown")
    for ts in tenant_settlements:
        tenant = tenants_in_apt.get(ts.tenant)
        rent = tenant.rent_pln if tenant else 0.0

        transfers = [
            tr for tr in manager.transfers
            if tr.tenant == ts.tenant
            and tr.settlement_year == year
            and tr.settlement_month == month
        ]
        total_paid = sum(tr.amount_pln for tr in transfers)
        total_due = rent + ts.total_due_pln
        total_paid - total_due


    # --- Transfers ---
    all_apt_transfers = [
        tr for tr in manager.transfers
        if tr.tenant in tenants_in_apt
        and tr.settlement_year == year
        and tr.settlement_month == month
    ]

    print_subsection_header("Transfers Received")
    if all_apt_transfers:
        for _tr in all_apt_transfers:
            pass
    else:
        pass

    total_received = sum(tr.amount_pln for tr in all_apt_transfers)
    total_rent = sum(t.rent_pln for t in tenants_in_apt.values())
    total_due_all = total_rent + settlement.total_due_pln
    total_received - total_due_all




if __name__ == "__main__":
    parameters = Parameters()
    manager = Manager(parameters)
    x = 4
    if len(sys.argv) == x:
        apartment_key = sys.argv[1]
        year = int(sys.argv[2])
        month = int(sys.argv[3])
        display_monthly_settlement(manager, apartment_key, year, month)
    else:
        display_apartments(manager)
        display_tenants(manager)
