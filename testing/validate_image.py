import filetype

def main():
    kind = filetype.guess('banner.jpg')
    if kind is None:
        print('Cannot guess file type!')
        return

    print('File extension: %s' % kind.extension)
    print('File MIME type: %s' % kind.mime)
    if kind.mime == "image/jpeg":
        print("true")

if __name__ == '__main__':
    main()