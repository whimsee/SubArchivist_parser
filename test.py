import os
import base64
import json

def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


def convert_to_json(to_convert):
    encode = base64.b64encode(to_convert)
    to_utf = encode.decode('utf-8')
    return to_utf

for image_name in os.listdir("subs/Marginal_Prince/Season_1/"):
    if image_name.endswith(".jpg"):
        banner_name = "subs/Marginal_Prince/Season_1/banner.jpg"
        with open(banner_name, "rb") as image:
            f = image.read()
            c = bytes(f)
            encode = base64.b64encode(c)
            data = encode.decode('utf-8')
            # banner = {'image': encode} 
            print(is_jsonable(data))
            banner = {'image': ()'banner.png', data)}
            print(banner)
        #print(banner_name, "found jpg", banner)
    elif image_name.endswith(".png"):
        banner_name = "subs/Marginal_Prince/Season_1/banner.png"
        banner = {'image': open(banner_name, 'rb')}
        print(banner_name, "found jpg", banner)
    else:
        banner = None
    if banner != None:
        break

# print(banner)