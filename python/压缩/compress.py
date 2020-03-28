import gzip

data = b"bjfbjskdfkjsdhfbsdjkfsdf"
t = gzip.compress(data)
print(t)
data = gzip.decompress(t)
print(data)
