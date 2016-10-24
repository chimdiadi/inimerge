=====
Usage
=====

To use pyinimerge in a project::

    import pyinimerge

    ini = pyinimerge.IniConfigMerge()
    ini.append('/path/to/file1.ini')
    ini.append('/path/to/file2.ini')
    ini.append('/path/to/file3.ini')

    ini.write('/path/to/file-out.ini')
