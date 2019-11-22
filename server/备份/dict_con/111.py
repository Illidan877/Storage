class QWE():
    qwe = 1

    def list_all_member(self):
        for name, value in vars(self).items():
            print('%s=%s' % (name, value))


    def qqq(self):
        print()

QWE().qqq()
