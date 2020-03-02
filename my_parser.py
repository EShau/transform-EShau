from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix -
               takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
         ident: set the transform matrix to the identity matrix -
         scale: create a scale matrix,
                then multiply the transform matrix by the scale matrix -
                takes 3 arguments (sx, sy, sz)
         move: create a translation matrix,
                    then multiply the transform matrix by the translation matrix -
                    takes 3 arguments (tx, ty, tz)
         rotate: create a rotation matrix,
                 then multiply the transform matrix by the rotation matrix -
                 takes 2 arguments (axis, theta) axis should be x y or z
         apply: apply the current transformation matrix to the edge matrix
         display: clear the screen, then
                  draw the lines of the edge matrix to the screen
                  display the screen
         save: clear the screen, then
               draw the lines of the edge matrix to the screen
               save the screen to a file -
               takes 1 argument (file name)
         quit: end parsing
See the file script for an example of the file format
"""

def parse_file( fname, points, transform, screen, color ):
    with open(fname,'r') as fileReader:
        file_line = fileReader.readline().strip()
        while file_line != "":
            if file_line == "line":
                file_line = fileReader.readline().strip()
                ints = [int(x) for x in file_line.split(" ")]
                add_edge(points, ints[0], ints[1], ints[2], ints[3], ints[4], ints[5])
            elif file_line == "ident":
                ident(transform)
            elif file_line == "scale":
                file_line = fileReader.readline().strip()
                nums = [float(x) for x in file_line.split(" ")]
                scale = make_scale(nums[0], nums[1], nums[2])
                matrix_mult(scale, transform)
            elif file_line == "move":
                file_line = fileReader.readline().strip()
                ints = [int(x) for x in file_line.split(" ")]
                move = make_translate(ints[0], ints[1], ints[2])
                matrix_mult(move, transform)
            elif file_line == "rotate":
                file_line = fileReader.readline().strip()
                args = file_line.split(" ")
                if args[0] == "x":
                    rotate = make_rotX(float(args[1]))
                elif args[0] == "y":
                    rotate = make_rotY(float(args[1]))
                else:
                    rotate = make_rotZ(float(args[1]))
                matrix_mult(rotate, transform)
            elif file_line == "apply":
                matrix_mult(transform, points)
                for col in points:
                    for x in range(len(col)):
                        col[x] = int(col[x])
            elif file_line == "display":
                clear_screen(screen)
                draw_lines(points, screen, color)
                display(screen)
            elif file_line == "save":
                file_line = fileReader.readline().strip()
                clear_screen(screen)
                draw_lines(points, screen, color)
                save_extension(screen, file_line)
            else:
                break
            file_line = fileReader.readline().strip()
