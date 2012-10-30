from vec import vec2d

class Box():
    def __init__(self, name, size, resistance, boxes):
        self.name = name
        self.size = size*1.0
        self.resistance = resistance*1.0
        self.forces_with_locs = []
        self.forces_have_been_applied = False
        self.is_crushed = False
        self.resulting_forces = None
        self.associated_boxes = {'left': None, 'right': None}
        if len(boxes) == 0:
            pass
        elif len(boxes) == 2:
            self.associated_boxes = {'left': boxes[0], 'right': boxes[1]}
        else:
            raise ValueError('Length of argument boxes should be 0 or 2.')
    
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
        
        self.forces_have_been_applied = True
        self.resulting_forces (left_y_force, right_y_force)
        
    def reset_applied_forces(self):
        self.forces_have_been_applied = False
        self.forces_with_locs = []
        
    def apply_force_to_self(self, F, loc):
        self.forces_with_locs.append((F, loc))
        
    def apply_resulting_left_force_to_other_box(self, box, loc):
        left_force = self.get_resulting_forces()[0]
        box.apply_force(left_force, loc)
        
    def apply_resulting_left_force_to_other_box(self, box, loc):
        left_force = self.get_resulting_forces()[0]
        box.apply_force(left_force, loc)
        
    def print_box_info(self):
        forces = self.get_resulting_forces()
        print
        print '=========================================='
        print 'Info for %s of length %s and resistance %s' % (self.name, self.size, self.resistance)
        print
        print 'Applied forces:'
        for tup in self.forces_with_locs:
            print '%s at %s' % tup
        print 'Was crushed? %s' % self.is_crushed
        print
        print 'Resulting forces from %s: left %s; right %s' % (self.name, forces[0], forces[1])
        print '=========================================='
        print

class BoxStack():
    def __init__(self, first_box, boxes):
        self.first_box = first_box
        self.boxes = boxes
        
    def apply_forces_with_locations_to_system(self, FL):
        for tup in FL:
            self.first_box.apply_force_to_self(tup[0], tup[1])

def six_box_pyramid(F):
    '''
        6-box pyramid
        
              |__1_|
           |__2_||__3_|
        |__4_||__5_||__6_|
    '''
    
    b6 = Box('Box 6', 10, 5, [])
    b5 = Box('Box 5', 10, 5, [])
    b4 = Box('Box 4', 10, 5, [])
    b3 = Box('Box 3', 10, 5, [b5, b6])
    b2 = Box('Box 2', 10, 5, [b4, b5])
    b1 = Box('Box 1', 10, 5, [b2, b3])
    
    system = BoxStack(b1, [b1,b2,b3,b4,b5,b6])
    system.apply_forces_with_locations_to_system([(F, b1.size / 2)])
    
six_box_pyramid(vec2d(0, 20))
