from .models import Item


def check_stock(name):
    """Look up how many of an item we have and its price."""
    item = Item.objects.filter(name__iexact=name).first()

    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}

    return {
        "name": item.name,
        "quantity": item.quantity,
        "price": float(item.price),
    }


def list_items():
    """Return every item in the inventory."""
    items = Item.objects.all()

    return {
        "items": [
            {
                "name": i.name,
                "quantity": i.quantity,
                "price": float(i.price),
            }
            for i in items
        ]
    }


def add_item(name, quantity, price=0):
    """Create a new item, or add to an existing one's stock."""
    item = Item.objects.filter(name__iexact=name).first()

    if item is not None:
        item.quantity += quantity

        if price > 0:
            item.price = price

        item.save()

        return {
            "name": item.name,
            "quantity": item.quantity,
            "price": float(item.price),
            "created": False,
        }

    item = Item.objects.create(
        name=name,
        quantity=quantity,
        price=price,
    )

    return {
        "name": item.name,
        "quantity": item.quantity,
        "price": float(item.price),
        "created": True,
    }


def remove_stock(name, quantity):
    """Take a quantity out of stock."""
    item = Item.objects.filter(name__iexact=name).first()

    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}

    if quantity > item.quantity:
        return {
            "error": f"Cannot remove {quantity}. Only {item.quantity} in stock.",
            "name": item.name,
            "quantity": item.quantity,
        }

    item.quantity -= quantity
    item.save()

    return {
        "name": item.name,
        "quantity": item.quantity,
        "price": float(item.price),
    }


def delete_item(name):
    """Remove an item from the inventory entirely."""
    item = Item.objects.filter(name__iexact=name).first()

    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}

    item.delete()

    return {"deleted": name}


TOOL_DECLARATIONS = [
    {
        "type": "function",
        "name": "check_stock",
        "description": "Look up the current quantity and price of a single item. Use this when the user asks about stock, price, cost, or calculations involving an item.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item, e.g. 'Chocolate Bar'.",
                },
            },
            "required": ["name"],
        },
    },
    {
        "type": "function",
        "name": "list_items",
        "description": "Return every item in the inventory with its quantity and price. Use this when the user asks what is in stock generally or asks for a list.",
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "type": "function",
        "name": "add_item",
        "description": "Add an item to the inventory with its quantity and price. If the item already exists, add to its stock and update its price.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item, e.g. 'Chocolate Bar'.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "How many units to add. Must be positive.",
                },
                "price": {
                    "type": "number",
                    "description": "The price of one unit of the item.",
                },
            },
            "required": ["name", "quantity", "price"],
        },
    },
    {
        "type": "function",
        "name": "remove_stock",
        "description": "Reduce the quantity of an existing item. Use this when items are sold, shipped or used. This does NOT delete the item; it only lowers the number.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item, e.g. 'Chocolate Bar'.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "How many units to remove. Must be positive.",
                },
            },
            "required": ["name", "quantity"],
        },
    },
    {
        "type": "function",
        "name": "delete_item",
        "description": "Permanently remove an item and its record from the inventory entirely. This is destructive. Only use it when the user clearly wants the item gone, not when they want to reduce its quantity.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item to delete.",
                },
            },
            "required": ["name"],
        },
    },
]


TOOL_FUNCTIONS = {
    "check_stock": check_stock,
    "list_items": list_items,
    "add_item": add_item,
    "remove_stock": remove_stock,
    "delete_item": delete_item,
}