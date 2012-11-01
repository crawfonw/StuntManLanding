from vec import vec2d

def poll(_list):
    temp = _list[0]
    _list.remove(temp)
    return temp

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
    def __init__(self, initial_force, boxes, trajectory):
        self.initial_force = initial_force #for now this can only be a single vector
        self.boxes = boxes #must be in order by layers from top to bottom!
        self.trajectory = trajectory #list of boxes that the force will travel through, with locations of hit
        
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
            #no associated boxes beneath it ==> on ground
            if box.associated_boxes['left'] is None and box.associated_boxes['right'] is None:
                if box.resulting_forces is not None: #in case forces were not applied yet
                    v += box.resulting_forces[0]
                    v += box.resulting_forces[1]
        return v
        
    def prune_crushed_boxes(self):
        for box in self.boxes:
            if box.is_crushed:
                self.boxes.remove(box)
        
    def run_system(self):
        count = 1
        force = self.initial_force
        while (not self.all_boxes_crushed() and len(self.trajectory) > 0) or self.calculate_total_force_to_ground() == vec2d(0,0):
            box, loc = poll(self.trajectory)
            self.apply_force_to_box((fogrce, loc), box)
            
            print
            print '~~~~~~~~~~~~~~~~~~'
            print 'Iteration %s' % count
            for box in self.boxes:
                box.print_box_info()
            print '~~~~~~~~~~~~~~~~~~'
            print
            
            print 'Total force to ground: %s' % self.calculate_total_force_to_ground()
            self.prune_crushed_boxes()
            for box in self.boxes:
                box.reset_applied_forces()
            count += 1

#give boxes and locs in order of trajectory                

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
    
    system = BoxStack(F, [b1,b2,b3,b4,b5,b6], [(b1, b1.size/2), (b3, b3.size/2), (b5, b5.size)])
    system.run_system()
    
def weird_pyramid(F):
    ''' 
           |_____1____|
           |__2_||__3_|
        |__4_||__5_||__6_|
    '''
    
    b6 = Box('Box 6', 10, 5, [])
    b5 = Box('Box 5', 10, 5, [])
    b4 = Box('Box 4', 10, 5, [])
    b3 = Box('Box 3', 10, 5, [(b5, b5.size / 2), (b6, b6.size / 2)])
    b2 = Box('Box 2', 10, 5, [(b4, b4.size / 2), (b5, b5.size / 2)])
    b1 = Box('Box 1', 20, 5, [(b2, 0), (b3, b3.size)])
    
six_box_pyramid(vec2d(0, 40))
#weird_pyramid(vec2d(0, 80))
#F = 2550; C = ?
