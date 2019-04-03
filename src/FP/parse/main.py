import parseLinks
import tagPATH
if __name__ == "__main__":
    '''
    This is main script to parse HTML source codes to generated the following folders:
    1)parsed
    2)links
    3)tagpath
    '''
    folder = ''  # html folder name, it should be under ~/html
    hPATH = os.path.join(HOME, 'html', folder)
    if not os.path.exists(os.path.join(HOME, 'html', folder + '_links')):
        os.makedirs(os.path.join(HOME, 'html', folder + '_links'))
    if not os.path.exists(os.path.join(HOME, 'html', folder + '_parsed')):
        os.makedirs(os.path.join(HOME, 'html', folder + '_parsed'))
    if not os.path.exists(os.path.join(HOME,'html',folder+'_tagpath')):
        os.makedirs(os.path.join(HOME,'html',folder+'_tagpath'))

    # generate parsed folder
    parseLinks.parseDOM(folder)
    # generate links
    parseLinks.extractLinks(folder)
    # generate tagpaths
    tagPATH.extract_tag_path(folder)

    '''
    Then, once the script is done, check if every three folders are created under ~/html
    '''