import math


def domath(*args):
    nums = list(args)
    nums.remove(nums[0])
    nums = [int(x) for x in nums]
    if args[0] == "add" or args[0] == "a":
        return sum(nums)
    if args[0] == "subtract" or args[0] == "s":
        return nums[0] - nums[1]
    if args[0] == "multiply" or args[0] == "m":
        for x in nums:
            r = 1
            for x in nums:
                r = r * x
        return r
    if args[0] == "divide" or args[0] == "d":
        return nums[0] // nums[1]
