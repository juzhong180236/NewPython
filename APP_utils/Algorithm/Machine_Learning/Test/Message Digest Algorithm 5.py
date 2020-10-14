import hashlib

if __name__ == "__main__":
    # MD5
    # 对英文加密
    md5 = hashlib.md5()
    md5.update(b"This is a sentence.")
    md5.update(b"This is another sentence.")
    md5.update(b".")
    print(md5.digest())
    print("MD5：", md5.hexdigest())
    # 另一种写法
    hashlib.new('md5', b'123').hexdigest()
    # 对中文加密
    hashlib.md5("你好".encode("UTF-8")).hexdigest()
    print(type(hashlib.md5("你好".encode("UTF-8")).hexdigest()))
    print(hashlib.md5("你好".encode("UTF-8")).hexdigest())

    str1 = hashlib.md5('你好'.encode(encoding='GBK')).hexdigest()
    str2 = hashlib.md5('你好'.encode(encoding='GB2312')).hexdigest()
    str3 = hashlib.md5('你好'.encode(encoding='GB18030')).hexdigest()
    print(str1, str2, str3)

    # SHA1 Secure Hash Algorithm
    str4 = hashlib.sha1("你好".encode("UTF-8")).digest()
    str5 = hashlib.sha1("你好".encode("UTF-8")).hexdigest()
    print(str4)
    print(str5)
