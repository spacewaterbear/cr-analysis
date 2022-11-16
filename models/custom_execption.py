
# create an exception when regex failed
class RegexFailed(Exception):
    def __init__(self, regex_pattern, text):
        self.message = f"{self.__class__.__name__}: {regex_pattern=} not found in {text=}"
        super().__init__(self.message)


