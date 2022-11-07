from udpy import UrbanClient


def urban(arg1):
    print(arg1)
    ud = UrbanClient()
    defs = ud.get_definition(arg1)
    return f"Definition of {defs[0]}"
