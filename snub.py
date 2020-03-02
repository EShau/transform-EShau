from display import *
from draw import *
from my_parser import *
from matrix import *

screen = new_screen()
color = [ 255, 255, 255 ]
points = []
transform = new_matrix()

def square_root(x):
    return x**(1./2)

def cube_root(x):
    return x**(1./3)

T = (1 + cube_root(19 - 3 * square_root(33)) + cube_root(19 + 3 * square_root(33))) / 3
original = [1, 1 / T, T]

def all_permutations(original_list):
    all_lists = []
    for item_1 in original_list:
        remaining_list_1 = [x for x in original_list]
        remaining_list_1.remove(item_1)
        for sign_1 in range(-1,2,2):
            new_list = []
            new_list.append(sign_1 * item_1)
            for item_2 in remaining_list_1:
                remaining_list_2 = [x for x in remaining_list_1]
                remaining_list_2.remove(item_2)
                for sign_2 in range(-1,2,2):
                    new_list.append(sign_2 * item_2)
                    for sign_3 in range(-1,2,2):
                        new_list.append(sign_3 * remaining_list_2[0])
                        all_lists.append([x for x in new_list])
                        new_list.pop()
                    new_list.pop()
            new_list.pop()
    return all_lists

def is_even(permutation):
    pos_permutation = [abs(x) for x in permutation]
    count = 0
    for i in range(len(pos_permutation)):
        for j in range(i + 1, len(pos_permutation)):
            if pos_permutation[i] > pos_permutation[j]:
                count += 1
    return ((count + 1) % 2) == 0

def prod(list):
    product = 1
    for x in list:
        product *= x
    return product

def is_snub(all_lists):
    ok_lists = []
    for list in all_lists:
        if (prod(list) > 0 and is_even(list)) or (prod(list) < 0 and not is_even(list)):
            ok_lists.append(list)
    return ok_lists

def distance(point_1, point_2):
    return square_root((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2 + (point_1[2] - point_2[2])**2)

def make_edges(ok_lists):
    edges = []
    for point in ok_lists:
        remaining_points = [x for x in ok_lists]
        remaining_points.remove(point)
        remaining_points.sort(key=lambda x: distance(point,x))
        for i in range(5):
            edge = []
            edge.append(point)
            edge.append(remaining_points[i])
            edge.sort()
            if edge not in edges:
                edges.append(edge)
    return edges

all_lists = all_permutations(original)
ok_lists = is_snub(all_lists)
edges = make_edges(ok_lists)

scale = lambda x: [int(z + 200) for z in [y * 50 for y in x]]
for x in range(len(edges)):
    edges[x] = [scale(y) for y in edges[x]]

with open("other",'w+') as fileWriter:
    for edge in edges:
        fileWriter.write("line\n")
        str_edge_0 = [str(coordinate) for coordinate in edge[0]]
        str_edge_1 = [str(coordinate) for coordinate in edge[1]]
        fileWriter.write((" ").join(str_edge_0) + " ")
        fileWriter.write((" ").join(str_edge_1) + "\n")
    fileWriter.write("ident\n")
    fileWriter.write("scale\n")
    fileWriter.write("1.8 1.8 1.8\n")
    fileWriter.write("apply\n")
    fileWriter.write("ident\n")
    fileWriter.write("rotate\n")
    fileWriter.write("z 45\n")
    fileWriter.write("rotate\n")
    fileWriter.write("x 45\n")
    fileWriter.write("rotate\n")
    fileWriter.write("y 45\n")
    fileWriter.write("apply\n")
    fileWriter.write("ident\n")
    fileWriter.write("move\n")
    fileWriter.write("-180 140 -80\n")
    fileWriter.write("apply\n")
    fileWriter.write("display\n")
    fileWriter.write("save\n")
    fileWriter.write("pic.png\n")

parse_file( 'other', points, transform, screen, color )
