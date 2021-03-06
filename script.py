import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands, symbols ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)
  
  Should set num_frames and basename if the frames 
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.

  jdyrlandweaver
==================== """
def first_pass( commands ):
    
    global frames
    global basename
    global hasVary
    global hasF
    global hasB
    hasVary = False
    hasF = False
    hasB = False

    for c in commands:
        first = c[0]
        tail = c[1:]

        if (first == "vary"):
            hasVary = True
            
        if (first == "frames"):
            frames = tail[0]
            hasF = True

        if (first == "basename"):
            basename = tail[0]
            hasB = True

    if (hasVary and not hasF):
        print "vary is found, but frames is not"
        sys.exit()

    if (hasF and not hasB):
        print "Base name is base"
        basename = "base"
        
    
    return frames


"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go 
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value. 
  ===================="""
def second_pass( commands, num_frames ):
    #pass

    global knobs


    knobs = [{} for x in range(num_frames)]

    for c in commands:
        
        first = c[0]
        tail = c[1:]

        if (first == "vary"):
            name = tail[0]
            startF = tail[1]
            endF = tail[2]
            startV = tail[3]
            endV = tail[4]

            dFrame = endF - startF
            dVal = endV - startV

            ratio = dVal / dFrame * 1.0

            inc = startV
            m = 1

            for i in range(startF, endF+m, m):
                knobs[i][name] = inc
                inc = startV + (m * ratio)


    return knobs

    

def run(filename):
    """
    This function runs an mdl script
    """

    global frames
    global basename
    global hasVary
    global hasF
    global hasB
    global knob
    
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = []
    step = 0.1

    parsed = = mdl.parseFile(filename)

    (commands, symbols) = parsed

    first_pass(commands);
    second_pass(commands);
    
    for command in commands:
        print command
        c = command[0]
        args = command[1:]

        if c == 'box':
            add_box(tmp,
                    args[0], args[1], args[2],
                    args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
        elif c == 'sphere':
            add_sphere(tmp,
                       args[0], args[1], args[2], args[3], step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
        elif c == 'torus':
            add_torus(tmp,
                      args[0], args[1], args[2], args[3], args[4], step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
        elif c == 'move':
            tmp = make_translate(args[0], args[1], args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        elif c == 'scale':
            tmp = make_scale(args[0], args[1], args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        elif c == 'rotate':
            theta = args[1] * (math.pi/180)
            if args[0] == 'x':
                tmp = make_rotX(theta)
            elif args[0] == 'y':
                tmp = make_rotY(theta)
            else:
                tmp = make_rotZ(theta)
            matrix_mult( stack[-1], tmp )
            stack[-1] = [ x[:] for x in tmp]
            tmp = []
        elif c == 'push':
            stack.append([x[:] for x in stack[-1]] )
        elif c == 'pop':
            stack.pop()
        elif c == 'display':
            display(screen)
        elif c == 'save':
            save_extension(screen, args[0])
