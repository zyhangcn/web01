class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        print(value)
        return int(value)



    def to_url(self, value):
        print(value,"to_url")
        return '%04d' % value