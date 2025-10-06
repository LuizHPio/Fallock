from packages.Vector2 import Vector2


class Vector2Tester:
    def __init__(self):
        pass

    def test01(self) -> bool:
        tryList: list[bool] = []

        posVector = Vector2(2, 2)
        posVector.x += 1
        posVector.y += 2

        if posVector.x == 3:
            tryList.append(True)
        else:
            tryList.append(False)
        if posVector.y == 4:
            tryList.append(True)
        else:
            tryList.append(False)

        for comparison in tryList:
            if not comparison:
                return False
        return True


if __name__ == "__main__":
    tester = Vector2Tester()
    print(f'Test 01 status: {"Success" if tester.test01() else "Failure"}')
