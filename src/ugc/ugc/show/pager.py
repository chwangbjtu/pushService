import math

class Pager(object):
    PAGE_RANGE = 5
    def __init__(self, page, total):
        self.page = int(page)
        self.total = int(total)
        self.range = int(Pager.PAGE_RANGE)

    def get_page_items(self):
        start = 1
        middle = int(math.ceil(float(self.range) / 2))
        if self.page <= middle:
            start = 1
        elif self.page > middle and self.page <= self.total - self.range + middle:
            start = self.page + middle - self.range
        else:
            start = self.total - self.range + 1
        
        return range(start, start + self.range)

if __name__ == "__main__":
    total = 20
    for page in range(1, total + 1):
        items = Pager(page, total).get_page_items()
        print '%s: [%s]' % (page, " ".join((str(i) for i in items)))
