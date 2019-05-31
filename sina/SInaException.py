
class SinaException(Exception):
    def __init__(self, ErrorObj):
        super().__init__(self)  # 初始化父类
        self.errorObj = ErrorObj

    # def __str__(self):
    #     return self.errorinfo



if __name__ == "__main__":
    try:
        raise SinaException("========")
    except Exception as e:
        print(e.errorObj)