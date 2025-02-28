import filetype
import os

def main():
    kind = filetype.guess('banner.temp')
    if kind is None:
        print('Cannot guess file type!')
        return

    print('File extension: %s' % kind.extension)
    print('File MIME type: %s' % kind.mime)
    if kind.mime == "image/jpeg":
        print("true")
        os.rename('banner.temp', 'banner.jpg')

if __name__ == '__main__':
    main()