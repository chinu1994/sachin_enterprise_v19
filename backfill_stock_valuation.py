import xmlrpc.client


# ============================================================
# ODOO CONNECTION
# ============================================================

ODOO_URL = "http://localhost:8521"
DB_NAME = "sachin_15sep_db"

USERNAME = "admin"
PASSWORD = "admin"


# ============================================================
# COMPANY FILTER
# ============================================================

# SACHIN ENTERPRISES = Company ID 2
COMPANY_ID = 1


# ============================================================
# XML-RPC CONNECTION
# ============================================================

common = xmlrpc.client.ServerProxy(
    f"{ODOO_URL}/xmlrpc/2/common"
)

uid = common.authenticate(
    DB_NAME,
    USERNAME,
    PASSWORD,
    {},
)

if not uid:
    raise Exception(
        "Odoo XML-RPC authentication failed. "
        "Please check DB name, username and password."
    )


print("=" * 80)
print("ODOO XML-RPC CONNECTED SUCCESSFULLY")
print("=" * 80)
print(f"URL      : {ODOO_URL}")
print(f"DB       : {DB_NAME}")
print(f"User     : {USERNAME}")
print(f"UID      : {uid}")
print("=" * 80)


models = xmlrpc.client.ServerProxy(
    f"{ODOO_URL}/xmlrpc/2/object"
)


# ============================================================
# EXECUTE HELPER
# ============================================================

def execute(model, method, *args):
    return models.execute_kw(
        DB_NAME,
        uid,
        PASSWORD,
        model,
        method,
        args,
    )


# ============================================================
# GET COMPANY
# ============================================================

print("\nFinding company...")

company_data = execute(
    "res.company",
    "read",
    [COMPANY_ID],
    [
        "name",
        "custom_stock_valuation_enabled",
    ],
)

if not company_data:
    raise Exception(
        f"Company not found: ID {COMPANY_ID}"
    )


company_record = company_data[0]

COMPANY_NAME = company_record.get("name")

valuation_enabled = company_record.get(
    "custom_stock_valuation_enabled"
)


print(f"Selected Company : {COMPANY_NAME}")
print(f"Company ID       : {COMPANY_ID}")


# ============================================================
# CHECK CUSTOM STOCK VALUATION
# ============================================================

if not valuation_enabled:
    raise Exception(
        f"Custom Stock Valuation is disabled for "
        f"company: {COMPANY_NAME}"
    )


print(
    "Custom Stock Valuation : ENABLED"
)


# ============================================================
# FIND DONE PICKINGS
# FOR SELECTED COMPANY ONLY
# ============================================================

print("\nSearching done stock pickings...")

picking_ids = execute(
    "stock.picking",
    "search",
    [
        ("state", "=", "done"),
        ("company_id", "=", COMPANY_ID),
    ],
)

total_done_pickings = len(picking_ids)


print(
    f"Done pickings for {COMPANY_NAME}: "
    f"{total_done_pickings}"
)

print("-" * 80)


# ============================================================
# COUNTERS
# ============================================================

internal_skipped = 0
already_valued_moves = 0
valuation_created_or_linked = 0
unresolved_moves = 0
error_moves = 0


# ============================================================
# PROCESS PICKINGS
# ============================================================

for picking_id in picking_ids:

    # --------------------------------------------------------
    # READ PICKING
    # --------------------------------------------------------

    picking_data = execute(
        "stock.picking",
        "read",
        [picking_id],
        [
            "name",
            "state",
            "company_id",
            "picking_type_id",
            "move_ids",
        ],
    )

    if not picking_data:
        continue

    picking = picking_data[0]

    picking_name = picking.get("name")

    company = picking.get("company_id")
    picking_type = picking.get("picking_type_id")

    company_id = (
        company[0]
        if company
        else False
    )

    company_name = (
        company[1]
        if company
        else "Unknown"
    )

    picking_type_id = (
        picking_type[0]
        if picking_type
        else False
    )


    # --------------------------------------------------------
    # SAFETY COMPANY CHECK
    # --------------------------------------------------------

    if company_id != COMPANY_ID:

        print(
            f"[SKIP - OTHER COMPANY] "
            f"{picking_name}"
        )

        continue


    # --------------------------------------------------------
    # GET PICKING TYPE CODE
    # --------------------------------------------------------

    picking_type_code = False

    if picking_type_id:

        picking_type_data = execute(
            "stock.picking.type",
            "read",
            [picking_type_id],
            ["code"],
        )

        if picking_type_data:

            picking_type_code = (
                picking_type_data[0].get("code")
            )


    # --------------------------------------------------------
    # SKIP INTERNAL TRANSFERS
    # --------------------------------------------------------

    if picking_type_code == "internal":

        internal_skipped += 1

        print(
            f"[SKIP - INTERNAL] "
            f"{picking_name} | "
            f"Company: {company_name}"
        )

        continue


    # --------------------------------------------------------
    # GET DONE MOVES
    # --------------------------------------------------------

    move_ids = picking.get("move_ids", [])

    if not move_ids:
        continue


    move_data = execute(
        "stock.move",
        "read",
        move_ids,
        [
            "id",
            "state",
            "product_id",
            "quantity",
            "valuation_move_id",
        ],
    )


    done_moves = [
        move
        for move in move_data
        if move.get("state") == "done"
    ]


    if not done_moves:
        continue


    # --------------------------------------------------------
    # FIND MOVES WITHOUT VALUATION
    # --------------------------------------------------------

    missing_moves = []

    for move in done_moves:

        valuation_move = move.get(
            "valuation_move_id"
        )

        if valuation_move:

            already_valued_moves += 1

        else:

            missing_moves.append(move)


    # --------------------------------------------------------
    # NOTHING TO BACKFILL
    # --------------------------------------------------------

    if not missing_moves:

        print(
            f"[ALREADY DONE] "
            f"{picking_name} | "
            f"All done moves already have valuation."
        )

        continue


    # --------------------------------------------------------
    # PROCESS MISSING MOVES
    # --------------------------------------------------------

    print(
        f"\n[PROCESSING] "
        f"{picking_name} | "
        f"Missing valuation moves: "
        f"{len(missing_moves)}"
    )


    for move in missing_moves:

        move_id = move.get("id")

        product = move.get(
            "product_id"
        )

        quantity = move.get(
            "quantity"
        )

        product_name = (
            product[1]
            if product
            else "Unknown Product"
        )


        print(
            f"  -> Move ID: {move_id} | "
            f"Product: {product_name} | "
            f"Qty: {quantity}"
        )


        # ----------------------------------------------------
        # CALL ODOO BACKFILL METHOD
        # ----------------------------------------------------

        try:

            result = execute(
                "stock.move",
                "backfill_custom_stock_valuation",
                [move_id],
            )


            # ------------------------------------------------
            # CHECK RESULT
            # ------------------------------------------------

            if not result:

                unresolved_moves += 1

                print(
                    f"     [WARNING] "
                    f"Backfill returned False "
                    f"for Move {move_id}"
                )

                continue


            # ------------------------------------------------
            # READ VALUATION MOVE AFTER PROCESSING
            # ------------------------------------------------

            valuation_data = execute(
                "stock.move",
                "read",
                [move_id],
                [
                    "valuation_move_id",
                ],
            )


            if not valuation_data:

                unresolved_moves += 1

                print(
                    f"     [WARNING] "
                    f"Unable to read valuation "
                    f"for Move {move_id}"
                )

                continue


            valuation_move = (
                valuation_data[0].get(
                    "valuation_move_id"
                )
            )


            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            if valuation_move:

                valuation_created_or_linked += 1

                print(
                    f"     [OK] Valuation JE: "
                    f"{valuation_move[1]} "
                    f"(ID {valuation_move[0]})"
                )

            else:

                unresolved_moves += 1

                print(
                    f"     [WARNING] "
                    f"No valuation created "
                    f"for Move {move_id}"
                )


        # ----------------------------------------------------
        # XML-RPC ERROR
        # ----------------------------------------------------

        except xmlrpc.client.Fault as error:

            error_moves += 1

            print(
                f"     [XML-RPC ERROR] "
                f"Move {move_id}"
            )

            print(
                f"     {error}"
            )


        # ----------------------------------------------------
        # GENERAL ERROR
        # ----------------------------------------------------

        except Exception as error:

            error_moves += 1

            print(
                f"     [ERROR] "
                f"Move {move_id}: {error}"
            )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")

print("=" * 80)
print("CUSTOM STOCK VALUATION - XML-RPC BACKFILL COMPLETED")
print("=" * 80)

print(
    f"Company                         : "
    f"{COMPANY_NAME}"
)

print(
    f"Company ID                      : "
    f"{COMPANY_ID}"
)

print(
    f"Total done pickings             : "
    f"{total_done_pickings}"
)

print(
    f"Internal pickings skipped       : "
    f"{internal_skipped}"
)

print(
    f"Moves already having valuation  : "
    f"{already_valued_moves}"
)

print(
    f"Valuation created/linked        : "
    f"{valuation_created_or_linked}"
)

print(
    f"Unresolved moves                : "
    f"{unresolved_moves}"
)

print(
    f"Error moves                     : "
    f"{error_moves}"
)

print("=" * 80)
print("BACKFILL FINISHED")
print("=" * 80)