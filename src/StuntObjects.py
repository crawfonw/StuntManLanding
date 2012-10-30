from vec import vec2d

class Box():
    def __init__(self, size, resistance):
        '''
            vectors_with_locs - list of (vec2d, x-loc)
            x-loc -> 0 = left of box, x0 = x0 units to right
        '''
        self.size = size*1.0
        self.resistance = resistance*1.0
        self.forces_with_locs = []
        self.is_crushed = False
        
    def get_resulting_forces(self):
        left_y_force = vec2d(0,0)
        right_y_force = vec2d(0,0)
        for force in self.forces_with_locs:
            if force[1] == 0:
                left_y_force.y += force[0].y
            elif force[1] == self.size:
                right_y_force.y += force[0].y
            else:
                right_y_force.y += force[0].y * (force[1]/self.size)
                left_y_force.y += force[0].y * (1 - force[1]/self.size)
        left_y_force.y = max(left_y_force.y - self.resistance, 0)
        right_y_force.y = max(right_y_force.y - self.resistance, 0)
        if left_y_force.y > 0 or right_y_force.y > 0:
            self.is_crushed = True
        return (left_y_force, right_y_force)
        
    def apply_force_to_box(self, F, loc):
        self.forces_with_locs.append((F, loc))
        
def print_box_info(box_name, box, forces):
    print
    print '=========================================='
    print 'Info for %s of length %s and resistance %s' % (box_name, box.size, box.resistance)
    print
    print 'Applied forces:'
    for tup in box.forces_with_locs:
        print '%s at %s' % tup
    print 'Was crushed? %s' % box.is_crushed
    print
    print 'Resulting forces from %s: left %s; right %s' % (box_name, forces[0], forces[1])
    print '=========================================='
    print

def six_box_pyramid(F):
    '''
        6-box pyramid
        
              |__1_|
           |__2_||__3_|
        |__4_||__5_||__6_|
    '''
    
    b1 = Box(10, 5)
    b2 = Box(10, 5)
    b3 = Box(10, 5)
    
    b1.apply_force_to_box(F, 0)
    b1.apply_force_to_box(F, b1.size)
    b1_forces = b1.get_resulting_forces()
    print_box_info('Box 1', b1, b1_forces)
    
    b2.apply_force_to_box(b1_forces[0], b2.size / 2)
    b3.apply_force_to_box(b1_forces[1], b3.size / 2)
    b2_forces = b2.get_resulting_forces()
    b3_forces = b3.get_resulting_forces()
    print_box_info('Box 2', b2, b2_forces)
    print_box_info('Box 3', b3, b3_forces)
    
    b4 = Box(10, 5)
    b5 = Box(10, 5)
    b6 = Box(10, 5)
    b4.apply_force_to_box(b2_forces[0], b4.size / 2)
    b5.apply_force_to_box(b2_forces[1], b5.size / 2)
    b5.apply_force_to_box(b3_forces[0], b5.size / 2)
    b6.apply_force_to_box(b3_forces[1], b6.size / 2)
    b4_forces = b4.get_resulting_forces()
    b5_forces = b5.get_resulting_forces()
    b6_forces = b6.get_resulting_forces()
    print_box_info('Box 4', b4, b4_forces)
    print_box_info('Box 5', b5, b5_forces)
    print_box_info('Box 6', b6, b6_forces)
    
six_box_pyramid(vec2d(0, 20))
