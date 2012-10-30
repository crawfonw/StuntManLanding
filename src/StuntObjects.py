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
    
    def apply_force(self, F, loc):
        self.forces_with_locs.append((F, loc))
    
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
        
        self.resulting_forces = (left_y_force, right_y_force)
        
    def reset_applied_forces(self):
        self.forces_have_been_applied = False
        self.forces_with_locs = []
        self.resulting_forces = None
        
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
        print 'Resulting forces from %s: left %s; right %s' % (self.name, self.resulting_forces[0], self.resulting_forces[1])
        print '=========================================='
        print

class BoxStack():
    def __init__(self, initial_force_and_loc, boxes):
        self.force_and_loc = initial_force_and_loc #for now this can only be a single vector
        self.boxes = boxes #must be in order by layers from top to bottom!
        
    def apply_force_to_box(self, FL, box):
        box.apply_force(FL[0], FL[1])
        box.get_resulting_forces()
        if box.associated_boxes['left'] is not None and box.associated_boxes['right'] is not None:
            left = box.associated_boxes['left']
            self.apply_force_to_box((box.resulting_forces[0], left[1]), left[0])
            right = box.associated_boxes['right']
            self.apply_force_to_box((box.resulting_forces[1], right[1]), right[0])
    
    def all_boxes_crushed(self):
        for box in self.boxes:
            if not box.is_crushed:
                return False
        return True
    
    def calculate_total_force_to_ground(self):
        v = vec2d(0,0)
        for box in self.boxes:
            if box.associated_boxes['left'] is None:
                #if no associated boxes we can just assume they are on the ground
                v += box.resulting_forces[0]
            if box.associated_boxes['right'] is None:
                #if no associated boxes we can just assume they are on the ground
                v += box.resulting_forces[1]
        return v
                

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
    b3 = Box('Box 3', 10, 5, [(b5, b5.size / 2), (b6, b6.size / 2)])
    b2 = Box('Box 2', 10, 5, [(b4, b4.size / 2), (b5, b5.size / 2)])
    b1 = Box('Box 1', 10, 5, [(b2, b2.size / 2), (b3, b3.size / 2)])
    
    system = BoxStack((F, b1.size / 2), [b1,b2,b3,b4,b5,b6])
    system.apply_force_to_box((F, b1.size / 2), b1)
    for box in system.boxes:
        box.print_box_info()
    print system.all_boxes_crushed()
    print system.calculate_total_force_to_ground()
    
six_box_pyramid(vec2d(0, 80))
