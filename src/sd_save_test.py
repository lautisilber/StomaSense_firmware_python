from libs.sdcard_helper import SD

a = "Hi\n"

#with SD() as sd:
#    with sd.open('test.txt', 'w') as f:
#        f.write(a)
        
with SD() as sd:
    with sd.open('W0.TXT', 'r') as f:
        print(f.read())
