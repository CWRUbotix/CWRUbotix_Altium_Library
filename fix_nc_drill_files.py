import sys

import tkinter as tk
from tkinter import filedialog

def fix_number_str(s, whole, decimal, mode):
    retval = ''
    sign_char = ''
    if s[0] == '-':
        sign_char = '-'
        s = s[1:]

    digits = 0
    if mode == 'TZ':
        while len(s) < decimal:
            s = '0' + s
        for i in range(len(s), 0, -1):
            c = s[i - 1]
            retval = c + retval
            digits += 1
            if digits == decimal:
                retval = '.' + retval
    elif mode == 'LZ':
        for i in range(0, len(s)):
            retval = retval + s[i]
            digits += 1
            if digits == whole:
                retval = retval + '.'
    else:
        # mode was probably NONE
        retval = s
    if retval[0] == '.':
        retval = '0' + retval
    
    retval = sign_char + retval
    
    return retval


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.fname = None
        self.create_widgets()

    def create_widgets(self):
        grid_row = 0

        self.open_file_btn = tk.Button(self, text="...", command=self.open_file)
        self.open_file_btn.grid(column=0, row=grid_row)
        grid_row += 1
        
        self.fix_file = tk.Button(self, text="Fix File", command=self.fix_file)
        self.fix_file.grid(column=0, row=grid_row)
        grid_row += 1

        self.quit_btn = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit_btn.grid(column=0, row=grid_row)
    
    def open_file(self):
        self.fname = tk.filedialog.askopenfilename()
    
    def fix_file(self):
        if self.fname == None:
            return
        try:
            in_header = False
            whole_digits = 2
            decimal_digits = 5
            number_mode = "NONE"
            f = open(self.fname, 'r') # open for read and write
            parts = self.fname.split('.')
            self.out_fname = parts[0] + "_FIXED." + parts[1]
            fout = open(self.out_fname, 'w')
            for line in f:
                if "M48" in line:
                    in_header = True
                    fout.write(line)
                    continue
                if in_header:
                    if "FILE_FORMAT" in line:
                        parts = line.split('=')[1].split(':')
                        whole_digits = int(parts[0])
                        decimal_digits = int(parts[1])
                        print("Number format is {}:{}".format(whole_digits, decimal_digits))
                    elif '%' in line or 'M95' in line:
                        in_header = False
                    elif 'TZ' in line:
                        number_mode = 'TZ' # trailing zeros included
                    elif 'LZ' in line:
                        number_mode = 'LZ' # leading zeros included
                    fout.write(line)

                else:
                    new_line = line.strip()
                    if 'X' in line:
                        if 'Y' in line:
                            pass
                        parts = line.split('X')
                        more = parts[1].split('Y')
                        parts[0] = more[0]
                        if '.' not in parts[0]:
                            parts[0] = fix_number_str(parts[0].strip(), whole_digits, decimal_digits, number_mode)
                            new_line = "X{}".format(parts[0])
                        
                        if len(more) > 1:
                            parts[1] = more[1] # we have a Y part
                            if '.' not in parts[1]:
                                parts[1] = fix_number_str(parts[1].strip(), whole_digits, decimal_digits, number_mode)
                                new_line = "{}Y{}".format(new_line, parts[1])
                    
                        # fout.write(new_line + '\n')
                    elif 'Y' in line:
                        parts = line.split('Y')
                        if '.' not in parts[1]:
                            new_line = "Y{}".format(fix_number_str(parts[1].strip(), whole_digits, decimal_digits, number_mode))
                    
                    fout.write(new_line + '\n')
            

            fout.close()
            print("done fixing file")
            
        except IOError:
            pass
        
def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()