#!/usr/bin/python

import sys as S
import re as R

def open_tex_file(pathname):
    """
    open_tex_file(pathname)
    Opens a TeX file to a read-only filestream and returns the stream handle.
    """
    fs = open(pathname, 'rb')
    return fs

def open_output_file(pathname):
    """
    open_output_file(pathname)
    Opens a HTML output file.
    """
    fs = open(pathname, 'wb')
    return fs

def open_template(pathname):
    """
    open_template(pathname)
    
    """
    fs = open(pathname, 'rb')
    return fs

def return_base_name(filename):
    ret = ""
    ret = R.search(r'(\w*)\.\w*$', filename)
    ret = ret.group(1)
    return ret

def parse_tex_file(tex_file, output_file, template):
    """
    parse_tex_file(tex_file, output_file, template)
    """
    # Put the lines of the template into an array
    template_buffer = []
    for i in template:
        template_buffer.append(i)
    # Output the tex file as the replace line in the array
    replace_line = 0
    for i in range(len(template_buffer)):
        if "{{ REPLACE }}" in template_buffer[i]:
            replace_line = i
    # Put the lines of the texfile into an array
    texfile_buffer = []
    for i in tex_file:
        texfile_buffer.append(i)
    output_buffer = template_buffer
    del output_buffer[replace_line]
    for i in range(len(texfile_buffer)):
        output_buffer.insert(replace_line + i, texfile_buffer[i])
    for i in range(len(output_buffer)):
        output_file.write(output_buffer[i])
    return

if __name__ == "__main__":
    print("TeXParser")
    input_files = []
    if(len(S.argv) > 1):
        for i in range(len(S.argv) - 1):
            input_files.append(S.argv[i + 1])
            tex_file = open_tex_file(input_files[i])
            output_name = './output/' + return_base_name(input_files[i]) + '.html'
            output_file = open_output_file(output_name)
            template_file = open_template('./templates/base.html')
            parse_tex_file(tex_file, output_file, template_file)
            tex_file.close()
            template_file.close()
            output_file.close()
    else:
        print("Usage: %s [FILE]" % (S.argv[0]))
        print("Converts LaTeX files into HTML documents with MathJaX support.")
