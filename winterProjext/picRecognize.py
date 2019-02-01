import zxing
textimage = "1.jpg"
reader = zxing.BarCodeReader()
barcode = reader.decode(textimage)
print(barcode.parsed)
