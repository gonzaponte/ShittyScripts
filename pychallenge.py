
def ex6():
    import zipfile as z

    f = z.ZipFile('../Downloads/channel.zip')

    nothing = 90052
    ftemplate = lambda x: str(x) + '.txt'

    comments = []
    while True:
        line = f.read(ftemplate(nothing))
        comments.append( f.getinfo(ftemplate(nothing)).comment )
        nothing = line.split()[-1]
        if nothing == 'comments.': break

    print ''.join(comments)

def ex7():
    pass
