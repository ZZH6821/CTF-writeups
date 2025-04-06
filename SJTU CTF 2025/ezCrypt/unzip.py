import base64
import gzip

def gzip_unzip_base64(content):
    base64_data = base64.b64decode(content)
    bytes_decom = gzip.decompress(base64_data)
    str_unzip = bytes_decom.decode()
    return str_unzip
 
if __name__ == '__main__':
    str_test = "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"
    gzip_str = str_test
    gunzip_str = gzip_unzip_base64(gzip_str)
    print("原始字符串:{0} \n解压后对象:{1}".format(gzip_str, gunzip_str))