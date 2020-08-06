class Test:
    one = '1',
    two = '2',
    three = '3'

    def __str__(self):
        return '' + str (self.one) + '' + str(self.two) + '' + str(self.three)

test = Test()

print(test)
for attrs, value in test.__dict__.keys():
    print(str(attrs) + str(value))
    if value == '2':
        setattr(test,attrs, '5555')
print(test)